import logging
import aiodocker

from fastapi import HTTPException
from app import util


class JobExecutor:
    def __init__(self, resources):
        self.resources = resources
        self.docker_client = aiodocker.Docker()
        self.volume_name = util.get_random_str()
        self.container_name = util.get_random_str()

    async def setup_docker_volume(self):
        storage = util.convert_storage(self.resources.storage)
        try:
            await self.docker_client.volumes.create({
                'Name': self.volume_name,
                'Driver': 'local',
                'DriverOpts': {
                    'type': 'tmpfs',
                    'device': 'tmpfs',
                    'o': f'size={storage}'
                }
            })
            logging.info("docker volume has been setup successfully.")
        except aiodocker.exceptions.DockerError as e:
            raise HTTPException(status_code=400, detail=f"Error creating volume: {e}")

    async def volume_delete(self):
        try:
            await util.run_command(f"docker volume rm {self.volume_name}")
        except Exception as err:
            logging.info(f"error happens while deleting docker volume {err}")
        finally:
            pass

    async def setup_container_with_code(self, code):
        config = {
            'Image': 'python:3.9-slim',
            'Cmd': ['python', '-c', code],
            'HostConfig': {
                'NanoCPUs': self.resources.cpu * 1000000000,
                'Memory': util.get_ram_space(self.resources.ram),
                'DeviceRequests': [
                    {
                        'Driver': 'nvidia',
                        'Count': self.resources.gpu,
                        'Capabilities': [['gpu']]
                    }
                ] if self.resources.gpu > 0 else [],
                'Binds': [
                    f'{self.volume_name}:/mnt/volume'
                ]
            }
        }

        logging.info("setting up container")
        try:
            container = await self.docker_client.containers.create_or_replace(
                name=self.container_name, config=config
            )
        except Exception as err:
            logging.info(f"error happens while creating the container {err}")
            raise HTTPException(status_code=400, detail=f"Error creating container:")
        return container

    async def execute(self, code: str):
        logging.info("volume is being created")
        await self.setup_docker_volume()

        logging.info("container is being created")
        container = await self.setup_container_with_code(code)
        await container.start()
        await container.wait()

        logs = await container.log(stdout=True, stderr=True)

        await container.stop()
        await container.delete()

        logging.info("volume is being deleted")
        await self.volume_delete()
        return ''.join(logs)

    @classmethod
    def factory(cls, resources):
        return cls(resources=resources)
