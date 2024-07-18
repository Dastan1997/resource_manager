from fastapi import APIRouter

from app.models.schema import JobRequest, JobResponse
from app.services.job_executor import JobExecutor

router = APIRouter()


@router.post("/job", response_model=JobResponse)
async def execute_task(job: JobRequest):
    result = await JobExecutor.factory(resources=job.resources) \
        .execute(job.code)
    return JobResponse(status="success", output=result)
