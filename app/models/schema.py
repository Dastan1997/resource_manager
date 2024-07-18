from pydantic import BaseModel
from pydantic import Field
from app.config import settings


class Resources(BaseModel):
    cpu: str
    gpu: str
    ram: str
    storage: str


class JobRequest(BaseModel):
    job_type: str
    code: str
    resources: Resources


class JobResponse(BaseModel):
    status: str
    output: str
