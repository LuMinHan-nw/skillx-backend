from sqlalchemy.orm import Session

from app.models.notification import Notification


def notify(db: Session, user_id: int, message: str):
    db.add(Notification(user_id=user_id, message=message))
