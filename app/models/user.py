from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    phone = Column(String(20), nullable=True)
    bio = Column(String(500), nullable=True)
    profile_picture = Column(String(255), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, default=utc_now)

    skills = relationship("Skill", back_populates="tutor", foreign_keys="Skill.tutor_id")
    bookings = relationship("Booking", back_populates="learner")
    certificates = relationship("Certificate", back_populates="student")
    notifications = relationship("Notification", back_populates="user")
