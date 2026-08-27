from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.user import utc_now


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(255), nullable=False)
    is_read = Column(Boolean, nullable=False, default=False)
    sent_at = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="notifications")
