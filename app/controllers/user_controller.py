from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.feedback_schema import FeedbackResponse
from app.schemas.user_schema import UserResponse, UserUpdate
from app.services import user_service
from app.utils.response import success_response

from pathlib import Path
import secrets


UPLOAD_DIR = Path(__file__).resolve().parents[2] / "frontend" / "uploads"
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def update_profile(data: UserUpdate, db: Session, current_user: User):
    user = user_service.update_profile(db, current_user, data)
    return success_response(
        "Profile updated",
        UserResponse.model_validate(user).model_dump(),
    )


async def upload_picture(file: UploadFile, db: Session, current_user: User):
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only png, jpg, jpeg or webp images are allowed",
        )

    content = await file.read()
    if len(content) > 2 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image must be smaller than 2 MB",
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"user{current_user.id}_{secrets.token_hex(4)}{extension}"
    (UPLOAD_DIR / filename).write_bytes(content)

    user = user_service.set_profile_picture(
        db, current_user, f"/uploads/{filename}"
    )
    return success_response(
        "Profile picture updated",
        {"profile_picture": user.profile_picture},
    )


def public_profile(user_id: int, db: Session):
    result = user_service.public_profile(db, user_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    user, avg_rating, review_count, reviews = result
    return success_response(
        "Student profile",
        {
            "id": user.id,
            "name": user.name,
            "bio": user.bio,
            "profile_picture": user.profile_picture,
            "avg_rating": round(float(avg_rating), 2) if avg_rating else None,
            "review_count": review_count,
            "reviews": [
                FeedbackResponse.model_validate(r).model_dump() for r in reviews
            ],
        },
    )
