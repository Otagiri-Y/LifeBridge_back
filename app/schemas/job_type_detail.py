from pydantic import BaseModel

class JobTypeDetailUpdate(BaseModel):
    job_type_detail: str
