from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.user import utc_now


class SkillCategory(Base):
    __tablename__ = "skill_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    skills = relationship("Skill", back_populates="category")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    tutor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("skill_categories.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    proficiency = Column(String(20), nullable=True)
    session_duration_minutes = Column(Integer, default=60)
    status = Column(String(20), nullable=False, default="pending")
    date_listed = Column(DateTime, default=utc_now)

    tutor = relationship("User", back_populates="skills", foreign_keys=[tutor_id])
    category = relationship("SkillCategory", back_populates="skills")
    availability = relationship(
        "TutorAvailability", back_populates="skill", cascade="all, delete-orphan"
    )
    bookings = relationship("Booking", back_populates="skill")
    materials = relationship(
        "SkillMaterial", back_populates="skill", cascade="all, delete-orphan"
    )


class TutorAvailability(Base):
    __tablename__ = "tutor_availability"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    skill = relationship("Skill", back_populates="availability")
