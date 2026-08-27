from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.user import utc_now


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    submitted_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(150), nullable=False)
    message = Column(String(1000), nullable=False)
    status = Column(String(20), nullable=False, default="open")
    admin_response = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    resolved_at = Column(DateTime, nullable=True)

    student = relationship("User", foreign_keys=[submitted_by])
