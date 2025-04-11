from pydantic import BaseModel, EmailStr
from datetime import date

class UserCreate(BaseModel):
    name: str
    address: str
    birth_date: date
    email: EmailStr
    password: str
