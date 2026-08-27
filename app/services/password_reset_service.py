from sqlalchemy.orm import Session

from app.config import PASSWORD_RESET_WINDOW_MINUTES
from app.models.password_reset import PasswordResetRequest
from app.models.user import User, utc_now
from app.services import user_service


def request_reset(db: Session, email: str) -> PasswordResetRequest | str:
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        return "No account with that email"

    request = (
        db.query(PasswordResetRequest)
        .filter(PasswordResetRequest.user_id == user.id)
        .first()
    )
    if request is None:
        request = PasswordResetRequest(user_id=user.id)
        db.add(request)

    # A fresh request always restarts the clock, even if one was already
    # pending, approved or expired - one row per student, reused in place.
    request.status = "pending"
    request.requested_at = utc_now()
    request.approved_at = None
    request.completed_at = None
    db.commit()
    db.refresh(request)
    return request


def list_all(db: Session):
    return (
        db.query(PasswordResetRequest)
        .order_by(PasswordResetRequest.requested_at.desc())
        .all()
    )


def approve(db: Session, request_id: int) -> PasswordResetRequest | None:
    request = (
        db.query(PasswordResetRequest)
        .filter(PasswordResetRequest.id == request_id)
        .first()
    )
    if request is None:
        return None

    request.status = "approved"
    request.approved_at = utc_now()
    db.commit()
    db.refresh(request)
    return request


def effective_status(request: PasswordResetRequest) -> str:
    """Approved requests silently expire after the window - no background
    job needed, this is only ever checked at read/complete time."""
    if request.status == "approved":
        elapsed_minutes = (utc_now() - request.approved_at).total_seconds() / 60
        if elapsed_minutes > PASSWORD_RESET_WINDOW_MINUTES:
            return "expired"
    return request.status


# Read through effective_status rather than request.status, otherwise a request
# that was approved hours ago would still be accepted here.
def complete_reset(db: Session, email: str, new_password: str) -> str | None:
    """Returns an error message on failure, None on success."""
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        return "No account with that email"

    request = (
        db.query(PasswordResetRequest)
        .filter(PasswordResetRequest.user_id == user.id)
        .first()
    )
    if request is None or effective_status(request) != "approved":
        return "No approved reset in progress. Ask an admin to approve a new request."

    user_service.set_password(db, user, new_password)
    request.status = "completed"
    request.completed_at = utc_now()
    db.commit()
    return None
