from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255))
    industry = Column(String(100))
    company_address = Column(String(255))
    company_email = Column(String(255))
    operating_cf = Column(Integer)
    investing_cf = Column(Integer)
    financing_cf = Column(Integer)
    company_atmosphere = Column(String(100))
    company_age = Column(String(100))
    company_style = Column(String(100))
    customer = Column(String(100))
    corporate_philosophy = Column(Text)

    # Jobとのリレーション（逆方向定義も必要）
    jobs = relationship("Job", back_populates="company")
