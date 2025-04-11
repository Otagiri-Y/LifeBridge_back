from pydantic import BaseModel

class CompanyUpdate(BaseModel):
    company_name: str
