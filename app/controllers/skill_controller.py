from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.skill_schema import (
    AvailabilityCreate,
    CategoryResponse,
    SkillCreate,
    SkillResponse,
    SkillUpdate,
)
from app.services import skill_service
from app.utils.response import success_response


def _skill_data(skill, include_availability=False):
    item = SkillResponse.model_validate(skill).model_dump()
    item["category"] = skill.category.name if skill.category else None
    item["category_id"] = skill.category_id
    item["tutor"] = skill.tutor.name if skill.tutor else None
    item["tutor_id"] = skill.tutor_id
    if include_availability:
        item["availability"] = [
            {
                "id": slot.id,
                "day_of_week": slot.day_of_week,
                "start_time": str(slot.start_time),
                "end_time": str(slot.end_time),
            }
            for slot in skill.availability
        ]
    return item


def _get_owned_skill(skill_id: int, db: Session, current_user: User):
    skill = skill_service.get_skill(db, skill_id)
    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found"
        )
    if skill.tutor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only manage your own skills",
        )
    return skill


def list_skills(db: Session, category_id: int | None = None, search: str | None = None):
    skills = skill_service.list_approved_skills(db, category_id, search)
    return success_response(
        "Approved skills", [_skill_data(s) for s in skills]
    )


def list_categories(db: Session):
    categories = skill_service.list_categories(db)
    data = [CategoryResponse.model_validate(c).model_dump() for c in categories]
    return success_response("Skill categories", data)


def list_my_skills(db: Session, current_user: User):
    skills = skill_service.list_mine(db, current_user.id)
    return success_response(
        "My skills", [_skill_data(s, include_availability=True) for s in skills]
    )


def get_skill(skill_id: int, db: Session, current_user: User | None):
    skill = skill_service.get_skill(db, skill_id)
    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found"
        )
    if skill.status != "approved" and (
        current_user is None or skill.tutor_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found"
        )
    return success_response(
        "Skill detail", _skill_data(skill, include_availability=True)
    )


def create_skill(data: SkillCreate, db: Session, current_user: User):
    result = skill_service.create_skill(db, current_user, data)
    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result
        )
    return success_response(
        "Skill submitted for approval", _skill_data(result)
    )


def update_skill(skill_id: int, data: SkillUpdate, db: Session, current_user: User):
    skill = _get_owned_skill(skill_id, db, current_user)
    result = skill_service.update_skill(db, skill, data)
    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result
        )
    return success_response(
        "Skill updated and resubmitted for approval", _skill_data(result)
    )


def delete_skill(skill_id: int, db: Session, current_user: User):
    skill = _get_owned_skill(skill_id, db, current_user)
    result = skill_service.delete_skill(db, skill)
    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result
        )
    return success_response("Skill deleted")


def add_availability(skill_id: int, data: AvailabilityCreate, db: Session,
                     current_user: User):
    skill = _get_owned_skill(skill_id, db, current_user)
    result = skill_service.add_availability(db, skill, data)
    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=result
        )
    return success_response(
        "Availability added",
        {
            "id": result.id,
            "day_of_week": result.day_of_week,
            "start_time": str(result.start_time),
            "end_time": str(result.end_time),
        },
    )


def delete_availability(skill_id: int, slot_id: int, db: Session,
                        current_user: User):
    skill = _get_owned_skill(skill_id, db, current_user)
    if not skill_service.delete_availability(db, skill, slot_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability slot not found",
        )
    return success_response("Availability removed")
