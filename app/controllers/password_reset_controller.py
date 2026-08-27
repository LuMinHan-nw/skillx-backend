from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.password_reset_schema import (
    PasswordResetComplete,
    PasswordResetRequestCreate,
    PasswordResetResponse,
)
from app.services import password_reset_service
from app.utils.response import success_response


def request_reset(data: PasswordResetRequestCreate, db: Session):
    result = password_reset_service.request_reset(db, data.email)
    if isinstance(result, str):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result)
    return success_response(
        "Reset requested. An admin needs to approve it before you can set a "
        "new password."
    )


def complete_reset(data: PasswordResetComplete, db: Session):
    error = password_reset_service.complete_reset(db, data.email, data.new_password)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return success_response("Password updated. You can log in now.")


def list_all(db: Session):
    requests = password_reset_service.list_all(db)
    data = []
    for r in requests:
        item = PasswordResetResponse.model_validate(r).model_dump()
        item["status"] = password_reset_service.effective_status(r)
        item["student"] = r.student.name if r.student else None
        item["email"] = r.student.email if r.student else None
        data.append(item)
    return success_response("Password reset requests", data)


def approve(request_id: int, db: Session):
    request = password_reset_service.approve(db, request_id)
    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Request not found"
        )
    return success_response("Reset approved")
