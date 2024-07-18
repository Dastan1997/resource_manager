from pydantic import BaseModel
from pydantic import Field


class Resources(BaseModel):
    cpu: str = Field(pattern=r"^[0-9]+$")
    gpu: str = Field(pattern=r"^[0-9]+$")
    ram: str = Field(pattern=r"^[0-9]+(MB|GB)$")
    storage: str = Field(pattern=r"^[0-9]+GB$")


class JobRequest(BaseModel):
    task_type: str
    code: str
    resources: Resources


class JobResponse(BaseModel):
    status: str
    output: str
