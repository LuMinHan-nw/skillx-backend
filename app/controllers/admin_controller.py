from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.schemas.skill_schema import CategoryResponse, SkillResponse
from app.schemas.user_schema import UserResponse, UserUpdate
from app.services import admin_service
from app.utils.response import success_response


def pending_skills(db: Session):
    skills = admin_service.pending_skills(db)
    data = []
    for skill in skills:
        item = SkillResponse.model_validate(skill).model_dump()
        item["tutor"] = skill.tutor.name if skill.tutor else None
        item["category"] = skill.category.name if skill.category else None
        data.append(item)
    return success_response("Pending skills", data)


def review_skill(skill_id: int, approve: bool, db: Session, current_user: User):
    skill = admin_service.review_skill(db, skill_id, current_user, approve)
    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found"
        )
    return success_response(f"Skill {skill.status}")


def list_users(db: Session, search: str | None = None):
    users = admin_service.list_users(db, search)
    return success_response(
        "Students",
        [UserResponse.model_validate(u).model_dump() for u in users],
    )


def set_user_status(user_id: int, new_status: str, db: Session):
    user = admin_service.set_user_status(db, user_id, new_status)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )
    return success_response(f"Account {new_status}")


def update_user_info(user_id: int, data: UserUpdate, db: Session):
    user = admin_service.update_user_info(db, user_id, data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )
    return success_response(
        "Student information updated",
        UserResponse.model_validate(user).model_dump(),
    )


def list_feedback(db: Session):
    records = admin_service.list_feedback(db)
    data = []
    for f in records:
        data.append({
            "id": f.id,
            "booking_id": f.booking_id,
            "given_by": f.reviewer.name if f.reviewer else None,
            "given_to": f.reviewee.name if f.reviewee else None,
            "rating": f.rating,
            "comments": f.comments,
            "submitted_at": f.submitted_at,
        })
    return success_response("User feedback", data)


def create_category(data: CategoryCreate, db: Session):
    category = admin_service.create_category(db, data)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists",
        )
    return success_response(
        "Category created",
        CategoryResponse.model_validate(category).model_dump(),
    )


def update_category(category_id: int, data: CategoryUpdate, db: Session):
    category = admin_service.update_category(db, category_id, data)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return success_response(
        "Category updated",
        CategoryResponse.model_validate(category).model_dump(),
    )


def delete_category(category_id: int, db: Session):
    result = admin_service.delete_category(db, category_id)
    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result
        )
    return success_response("Category deleted")
