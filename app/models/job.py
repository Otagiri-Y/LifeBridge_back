from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    job_title = Column(String(100))
    company_job_type = Column(String(100))
    job_description = Column(Text)
    work_location = Column(String(100))
    work_hours = Column(String(100))
    salary = Column(Integer)
    number_of_openings = Column(Integer)
    skill_1 = Column(String(100))
    skill_2 = Column(String(100))
    skill_3 = Column(String(100))
    tag_1 = Column(String(100))
    tag_2 = Column(String(100))
    tag_3 = Column(String(100))
    employment_purpose = Column(String(100))
    expected_role = Column(String(100))

    # 外部キー関係（企業）
    company = relationship("Company", back_populates="jobs")
