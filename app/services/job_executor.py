import asyncio
from typing import Annotated


from app.models.schema import JobRequest

class JobExecutor:
    def __init__(self, resource):
        self.resource = resource

    async def execute(self, task: JobRequest) -> str:
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
