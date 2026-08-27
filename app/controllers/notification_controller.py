from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.notification_schema import NotificationResponse
from app.services import notification_service
from app.utils.response import success_response


def list_notifications(db: Session, current_user: User):
    notifications = notification_service.list_for_user(db, current_user.id)
    data = [
        NotificationResponse.model_validate(n).model_dump() for n in notifications
    ]
    return success_response("Notifications", data)


def mark_read(notification_id: int, db: Session, current_user: User):
    notification = notification_service.mark_read(db, notification_id, current_user.id)
    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    return success_response("Notification marked as read")
