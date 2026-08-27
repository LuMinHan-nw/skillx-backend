from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.skill import Skill, SkillCategory, TutorAvailability


def list_approved_skills(db: Session, category_id: int | None = None, search: str | None = None):
    query = db.query(Skill).filter(Skill.status == "approved")
    if category_id:
        query = query.filter(Skill.category_id == category_id)
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            Skill.name.ilike(pattern) | Skill.description.ilike(pattern)
        )
    return query.all()


def list_categories(db: Session):
    return db.query(SkillCategory).all()


def get_skill(db: Session, skill_id: int) -> Skill | None:
    return db.query(Skill).filter(Skill.id == skill_id).first()


def list_mine(db: Session, tutor_id: int):
    return db.query(Skill).filter(Skill.tutor_id == tutor_id).all()


def create_skill(db: Session, tutor, data) -> Skill | str:
    category = (
        db.query(SkillCategory).filter(SkillCategory.id == data.category_id).first()
    )
    if category is None:
        return "Category not found"

    skill = Skill(
        tutor_id=tutor.id,
        category_id=data.category_id,
        name=data.name,
        description=data.description,
        proficiency=data.proficiency,
        session_duration_minutes=data.session_duration_minutes,
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def update_skill(db: Session, skill: Skill, data) -> Skill | str:
    if data.category_id is not None:
        category = (
            db.query(SkillCategory)
            .filter(SkillCategory.id == data.category_id)
            .first()
        )
        if category is None:
            return "Category not found"
        skill.category_id = data.category_id
    if data.name is not None:
        skill.name = data.name
    if data.description is not None:
        skill.description = data.description
    if data.proficiency is not None:
        skill.proficiency = data.proficiency
    if data.session_duration_minutes is not None:
        skill.session_duration_minutes = data.session_duration_minutes

    skill.status = "pending"
    skill.approved_by = None
    db.commit()
    db.refresh(skill)
    return skill


def delete_skill(db: Session, skill: Skill) -> str | bool:
    if db.query(Booking).filter(Booking.skill_id == skill.id).count() > 0:
        return "Cannot delete a skill that has bookings"

    db.delete(skill)
    db.commit()
    return True


def add_availability(db: Session, skill: Skill, data) -> TutorAvailability | str:
    if data.end_time <= data.start_time:
        return "end_time must be after start_time"

    slot = TutorAvailability(
        skill_id=skill.id,
        day_of_week=data.day_of_week,
        start_time=data.start_time,
        end_time=data.end_time,
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot


def delete_availability(db: Session, skill: Skill, slot_id: int) -> bool:
    slot = (
        db.query(TutorAvailability)
        .filter(TutorAvailability.id == slot_id)
        .filter(TutorAvailability.skill_id == skill.id)
        .first()
    )
    if slot is None:
        return False

    db.delete(slot)
    db.commit()
    return True
