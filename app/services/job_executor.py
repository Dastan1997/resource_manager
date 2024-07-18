import asyncio
import aiodocker

from app.models.schema import JobRequest


class JobExecutor:
    def __init__(self, resources):
        self.resources = resources
        self.docker_client = aiodocker.Docker()
    def setup_docker_volume(self):
        pass
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
