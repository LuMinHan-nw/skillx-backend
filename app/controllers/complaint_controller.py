from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.complaint_schema import (
    ComplaintCreate,
    ComplaintResolve,
    ComplaintResponse,
)
from app.services import complaint_service
from app.utils.response import success_response


def submit(data: ComplaintCreate, db: Session, current_user: User):
    complaint = complaint_service.submit(db, current_user, data)
    return success_response(
        "Complaint submitted",
        ComplaintResponse.model_validate(complaint).model_dump(),
    )


def list_mine(db: Session, current_user: User):
    complaints = complaint_service.list_mine(db, current_user.id)
    return success_response(
        "My complaints",
        [ComplaintResponse.model_validate(c).model_dump() for c in complaints],
    )


def list_all(db: Session):
    complaints = complaint_service.list_all(db)
    data = []
    for c in complaints:
        item = ComplaintResponse.model_validate(c).model_dump()
        item["student"] = c.student.name if c.student else None
        data.append(item)
    return success_response("Complaints", data)


def resolve(complaint_id: int, data: ComplaintResolve, db: Session):
    complaint = complaint_service.resolve(db, complaint_id, data)
    if complaint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found"
        )
    return success_response(
        "Complaint resolved",
        ComplaintResponse.model_validate(complaint).model_dump(),
    )
