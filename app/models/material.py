from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.user import utc_now


class SkillMaterial(Base):
    __tablename__ = "skill_materials"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    stored_path = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime, default=utc_now)

    skill = relationship("Skill", back_populates="materials")
