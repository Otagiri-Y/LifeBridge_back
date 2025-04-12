from pydantic import BaseModel

class UserMatchingUpdate(BaseModel):
    atmosphere: str
    age_group: str
    work_style: str
    work_purpose: str
    ideal_role: str
    contribute: str
    personal_values: str
