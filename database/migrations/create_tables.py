import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from app.database import Base, engine
from app.models import (
    Booking,
    Certificate,
    Complaint,
    Feedback,
    Notification,
    PasswordResetRequest,
    Skill,
    SkillCategory,
    SkillMaterial,
    TutorAvailability,
    User,
)


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


if __name__ == "__main__":
    create_tables()
