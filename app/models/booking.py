from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.user import utc_now


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    learner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    cancel_reason = Column(String(255), nullable=True)
    meeting_link = Column(String(500), nullable=True)
    booked_at = Column(DateTime, default=utc_now)

    skill = relationship("Skill", back_populates="bookings")
    learner = relationship("User", back_populates="bookings")
    feedback = relationship("Feedback", back_populates="booking")
