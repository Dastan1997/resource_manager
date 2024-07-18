from fastapi import FastAPI
from app.api.endpoints import job_runner

app = FastAPI()

app.include_router(job_runner.router, tags=["task_handler"])
