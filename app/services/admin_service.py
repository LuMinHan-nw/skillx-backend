from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.feedback import Feedback
from app.models.skill import Skill, SkillCategory
from app.models.user import User
from app.services.notification_helper import notify


def pending_skills(db: Session):
    return db.query(Skill).filter(Skill.status == "pending").all()


def review_skill(db: Session, skill_id: int, admin, approve: bool) -> Skill | None:
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if skill is None:
        return None

    skill.status = "approved" if approve else "rejected"
    skill.approved_by = admin.id if approve else None
    notify(db, skill.tutor_id,
           f"Your skill '{skill.name}' was {skill.status} by the administrator.")
    db.commit()
    db.refresh(skill)
    return skill


def list_users(db: Session, search: str | None = None):
    query = db.query(User).filter(User.role == "student")
    if search:
        pattern = f"%{search}%"
        query = query.filter(User.name.ilike(pattern) | User.email.ilike(pattern))
    return query.all()


def set_user_status(db: Session, user_id: int, status: str) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or user.role != "student":
        return None

    user.status = status
    db.commit()
    db.refresh(user)
    return user


def update_user_info(db: Session, user_id: int, data) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or user.role != "student":
        return None

    if data.name is not None:
        user.name = data.name
    if data.phone is not None:
        user.phone = data.phone
    if data.bio is not None:
        user.bio = data.bio
    db.commit()
    db.refresh(user)
    return user


def create_category(db: Session, data) -> SkillCategory | None:
    existing = (
        db.query(SkillCategory).filter(SkillCategory.name == data.name).first()
    )
    if existing:
        return None

    category = SkillCategory(name=data.name, description=data.description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category_id: int, data) -> SkillCategory | None:
    category = (
        db.query(SkillCategory).filter(SkillCategory.id == category_id).first()
    )
    if category is None:
        return None

    if data.name is not None:
        category.name = data.name
    if data.description is not None:
        category.description = data.description
    db.commit()
    db.refresh(category)
    return category


def list_feedback(db: Session):
    return db.query(Feedback).order_by(Feedback.submitted_at.desc()).all()


def delete_category(db: Session, category_id: int) -> str | bool:
    category = (
        db.query(SkillCategory).filter(SkillCategory.id == category_id).first()
    )
    if category is None:
        return "Category not found"
    if db.query(Skill).filter(Skill.category_id == category_id).count() > 0:
        return "Cannot delete a category that has skills"

    db.delete(category)
    db.commit()
    return True
