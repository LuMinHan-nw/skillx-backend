from sqlalchemy.orm import Session

from app.models.notification import Notification


def list_for_user(db: Session, user_id: int):
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.sent_at.desc())
        .limit(20)
        .all()
    )


def mark_read(db: Session, notification_id: int, user_id: int) -> Notification | None:
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .filter(Notification.user_id == user_id)
        .first()
    )
    if notification is None:
        return None

    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification
