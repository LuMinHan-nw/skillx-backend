from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.user import utc_now


class PasswordResetRequest(Base):
    __tablename__ = "password_reset_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    status = Column(String(20), nullable=False, default="pending")
    requested_at = Column(DateTime, default=utc_now)
    approved_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    student = relationship("User", foreign_keys=[user_id])
