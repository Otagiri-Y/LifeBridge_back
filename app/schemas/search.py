from pydantic import BaseModel
from typing import Optional

class JobSchema(BaseModel):
    job_id: int
    company_id: int
    job_title: str
    company_job_type: Optional[str]
    job_description: Optional[str]
    work_location: Optional[str]
    work_hours: Optional[str]
    salary: Optional[int]
    number_of_openings: Optional[int]
    skill_1: Optional[str]
    skill_2: Optional[str]
    skill_3: Optional[str]
    tag_1: Optional[str]
    tag_2: Optional[str]
    tag_3: Optional[str]
    employment_purpose: Optional[str]
    expected_role: Optional[str]

    class Config:
        orm_mode = True
