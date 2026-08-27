from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.booking_schema import (
    BookingCancel,
    BookingCreate,
    BookingMeetingLink,
    BookingReschedule,
    BookingResponse,
)
from app.services import booking_service
from app.utils.response import success_response


def _booking_data(booking):
    item = BookingResponse.model_validate(booking).model_dump()
    item["skill"] = booking.skill.name if booking.skill else None
    item["tutor"] = booking.skill.tutor.name if booking.skill else None
    item["tutor_id"] = booking.skill.tutor_id if booking.skill else None
    item["learner"] = booking.learner.name if booking.learner else None
    return item


def _get_booking(booking_id: int, db: Session):
    booking = booking_service.get_booking(db, booking_id)
    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found"
        )
    return booking


def create_booking(data: BookingCreate, db: Session, current_user: User):
    result = booking_service.create_booking(db, current_user, data)
    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result
        )
    return success_response("Booking requested", _booking_data(result))


def list_my_bookings(db: Session, current_user: User):
    as_learner, as_tutor = booking_service.list_mine(db, current_user.id)
    return success_response(
        "My bookings",
        {
            "as_learner": [_booking_data(b) for b in as_learner],
            "as_tutor": [_booking_data(b) for b in as_tutor],
        },
    )


def accept(booking_id: int, db: Session, current_user: User):
    booking = _get_booking(booking_id, db)
    result = booking_service.set_status_by_tutor(
        db, booking, current_user, "confirmed", ("pending", "rescheduled")
    )
    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result
        )
    return success_response("Booking confirmed", _booking_data(result))


def decline(booking_id: int, db: Session, current_user: User):
    booking = _get_booking(booking_id, db)
    result = booking_service.set_status_by_tutor(
        db, booking, current_user, "declined", ("pending", "rescheduled")
    )
    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result
        )
    return success_response("Booking declined", _booking_data(result))


def complete(booking_id: int, db: Session, current_user: User):
    booking = _get_booking(booking_id, db)
    result = booking_service.set_status_by_tutor(
        db, booking, current_user, "completed", ("confirmed",)
    )
    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result
        )
    return success_response("Session marked as completed", _booking_data(result))


def cancel(booking_id: int, data: BookingCancel, db: Session, current_user: User):
    booking = _get_booking(booking_id, db)
    result = booking_service.cancel_booking(
        db, booking, current_user, data.reason
    )
    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result
        )
    return success_response("Booking cancelled", _booking_data(result))


def reschedule(booking_id: int, data: BookingReschedule, db: Session,
               current_user: User):
    booking = _get_booking(booking_id, db)
    result = booking_service.reschedule(db, booking, current_user, data)
    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result
        )
    return success_response("Booking rescheduled", _booking_data(result))


def set_meeting_link(booking_id: int, data: BookingMeetingLink, db: Session,
                     current_user: User):
    booking = _get_booking(booking_id, db)
    result = booking_service.set_meeting_link(
        db, booking, current_user, data.meeting_link
    )
    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result
        )
    return success_response("Meeting link saved", _booking_data(result))
