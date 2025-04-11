from pydantic import BaseModel

class JobTypeUpdate(BaseModel):
    job_type: str
