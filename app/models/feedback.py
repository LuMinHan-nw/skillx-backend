from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.user import utc_now


class Feedback(Base):
    __tablename__ = "feedback"
    __table_args__ = (
        UniqueConstraint("booking_id", "given_by", name="uq_feedback_once_per_reviewer"),
    )

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    given_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    given_to = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comments = Column(String(500), nullable=True)
    submitted_at = Column(DateTime, default=utc_now)

    booking = relationship("Booking", back_populates="feedback")
    reviewer = relationship("User", foreign_keys=[given_by])
    reviewee = relationship("User", foreign_keys=[given_to])
