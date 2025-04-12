from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    preference_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)
    atmosphere = Column(String(100))
    age_group = Column(String(100))
    work_style = Column(String(100))

    user = relationship("User", back_populates="preferences")
