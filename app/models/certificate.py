from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.user import utc_now


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    certificate_code = Column(String(50), unique=True, nullable=False)
    sessions_completed = Column(Integer, nullable=False)
    issued_at = Column(DateTime, default=utc_now)

    student = relationship("User", back_populates="certificates")
