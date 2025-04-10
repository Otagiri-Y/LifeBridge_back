from sqlalchemy import Column, Integer, String, Date
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    birth_date = Column(Date)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    last_company = Column(String)
    job_type = Column(String)
    job_type_detail = Column(String)
