from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.models.user import utc_now
from app.services.notification_helper import notify


def submit(db: Session, user, data) -> Complaint:
    complaint = Complaint(
        submitted_by=user.id,
        subject=data.subject,
        message=data.message,
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint


def list_mine(db: Session, user_id: int):
    return (
        db.query(Complaint)
        .filter(Complaint.submitted_by == user_id)
        .order_by(Complaint.created_at.desc())
        .all()
    )


def list_all(db: Session):
    return db.query(Complaint).order_by(Complaint.created_at.desc()).all()


def resolve(db: Session, complaint_id: int, data) -> Complaint | None:
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if complaint is None:
        return None

    complaint.status = "resolved"
    complaint.admin_response = data.admin_response
    complaint.resolved_at = utc_now()
    notify(db, complaint.submitted_by,
           f"Your complaint '{complaint.subject}' has been resolved.")
    db.commit()
    db.refresh(complaint)
    return complaint
