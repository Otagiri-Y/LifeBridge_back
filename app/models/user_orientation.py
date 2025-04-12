from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserOrientation(Base):
    __tablename__ = "user_orientation"

    orientation_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)
    work_purpose = Column(String(255))
    ideal_role = Column(String(255))
    contribute = Column(String(255))
    personal_values = Column(String(255))

    user = relationship("User", back_populates="orientation")
