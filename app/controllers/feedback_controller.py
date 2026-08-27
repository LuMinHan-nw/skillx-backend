from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.feedback_schema import FeedbackCreate, FeedbackResponse, FeedbackUpdate
from app.services import feedback_service
from app.utils.response import success_response


def submit(data: FeedbackCreate, db: Session, current_user: User):
    result = feedback_service.submit(db, current_user, data)
    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result
        )
    return success_response(
        "Feedback submitted",
        FeedbackResponse.model_validate(result).model_dump(),
    )


def update(feedback_id: int, data: FeedbackUpdate, db: Session, current_user: User):
    result = feedback_service.update(db, feedback_id, current_user, data)
    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result
        )
    return success_response(
        "Feedback updated",
        FeedbackResponse.model_validate(result).model_dump(),
    )


def pending(db: Session, current_user: User):
    bookings = feedback_service.pending_for_user(db, current_user.id)
    return success_response(
        "Sessions awaiting your review",
        [
            {
                "booking_id": b.id,
                "skill": b.skill.name,
                "session_date": str(b.session_date),
                "other_party": (
                    b.skill.tutor.name
                    if current_user.id == b.learner_id
                    else b.learner.name
                ),
            }
            for b in bookings
        ],
    )
