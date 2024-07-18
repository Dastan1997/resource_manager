import asyncio
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

    def setup_docker_container(self):
        pass

    @classmethod
    def factory(cls, resources):
        return cls(resources=resources)

    async def execute(self, code: str) -> str:
        """
        execute task inside docker container with resources specified in task.
        :param task:
        :return:
        """
        try:
            result = await execute_job(task.resources)
            return result
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail='timeout')
