from sqlalchemy.orm import Session

from app.config import CERTIFICATE_SESSION_TARGET
from app.models.booking import Booking
from app.models.skill import Skill
from app.services import certificate_service
from app.services.notification_helper import notify


def get_booking(db: Session, booking_id: int) -> Booking | None:
    return db.query(Booking).filter(Booking.id == booking_id).first()


def create_booking(db: Session, learner, data) -> Booking | str:
    skill = db.query(Skill).filter(Skill.id == data.skill_id).first()
    if skill is None or skill.status != "approved":
        return "Skill not found or not approved"
    if skill.tutor_id == learner.id:
        return "You cannot book your own skill"

    booking = Booking(
        skill_id=skill.id,
        learner_id=learner.id,
        session_date=data.session_date,
        start_time=data.start_time,
        end_time=data.end_time,
    )
    db.add(booking)
    notify(db, skill.tutor_id,
           f"New booking request from {learner.name} for '{skill.name}'.")
    db.commit()
    db.refresh(booking)
    return booking


def list_mine(db: Session, user_id: int):
    as_learner = (
        db.query(Booking)
        .filter(Booking.learner_id == user_id)
        .order_by(Booking.session_date.desc())
        .all()
    )
    as_tutor = (
        db.query(Booking)
        .join(Skill, Booking.skill_id == Skill.id)
        .filter(Skill.tutor_id == user_id)
        .order_by(Booking.session_date.desc())
        .all()
    )
    return as_learner, as_tutor


# Accept, decline and complete all follow the same shape, so they share one
# function. allowed_from is the set of statuses the booking may legally move
# out of, which is what stops a completed session being declined afterwards.
def set_status_by_tutor(db: Session, booking: Booking, tutor, new_status: str,
                        allowed_from: tuple) -> Booking | str:
    if booking.skill.tutor_id != tutor.id:
        return "Only the tutor of this skill can do this"
    if booking.status not in allowed_from:
        return f"Booking cannot move from '{booking.status}' to '{new_status}'"

    booking.status = new_status
    notify(db, booking.learner_id,
           f"Your booking for '{booking.skill.name}' is now {new_status}.")

    certificate = None
    if new_status == "completed":
        # The status set above has not been committed yet, so this booking is
        # still counted as not completed - hence the + 1 for the current one.
        completed = (
            db.query(Booking)
            .filter(Booking.learner_id == booking.learner_id)
            .filter(Booking.status == "completed")
            .count()
        ) + 1
        # Awarded on every multiple of the target, not just the first one.
        if completed % CERTIFICATE_SESSION_TARGET == 0:
            certificate = certificate_service.issue(
                db, booking.learner_id, completed
            )

    db.commit()
    db.refresh(booking)
    if certificate is not None:
        notify(db, booking.learner_id,
               "Congratulations! You earned a certificate for "
               f"completing {CERTIFICATE_SESSION_TARGET} sessions.")
        db.commit()
    return booking


def set_meeting_link(db: Session, booking: Booking, tutor, link: str) -> Booking | str:
    if booking.skill.tutor_id != tutor.id:
        return "Only the tutor of this skill can do this"
    if booking.status in ("completed", "cancelled", "declined"):
        return f"Cannot set a meeting link on a '{booking.status}' booking"

    booking.meeting_link = link
    notify(db, booking.learner_id,
           f"{tutor.name} added a meeting link for '{booking.skill.name}'.")
    db.commit()
    db.refresh(booking)
    return booking


def cancel_booking(db: Session, booking: Booking, user, reason) -> Booking | str:
    if booking.learner_id != user.id and booking.skill.tutor_id != user.id:
        return "Only the learner or the tutor of this booking can cancel it"
    if booking.status in ("completed", "cancelled", "declined"):
        return f"Booking cannot be cancelled from '{booking.status}'"

    booking.status = "cancelled"
    booking.cancel_reason = reason
    other_id = (booking.skill.tutor_id
                if user.id == booking.learner_id else booking.learner_id)
    notify(db, other_id,
           f"{user.name} cancelled the booking for '{booking.skill.name}'.")
    db.commit()
    db.refresh(booking)
    return booking


def reschedule(db: Session, booking: Booking, user, data) -> Booking | str:
    if booking.learner_id != user.id and booking.skill.tutor_id != user.id:
        return "Only the learner or the tutor of this booking can reschedule it"
    if booking.status in ("completed", "cancelled", "declined"):
        return f"Booking cannot be rescheduled from '{booking.status}'"

    booking.session_date = data.session_date
    booking.start_time = data.start_time
    booking.end_time = data.end_time
    booking.status = "rescheduled"
    other_id = (booking.skill.tutor_id
                if user.id == booking.learner_id else booking.learner_id)
    notify(db, other_id,
           f"The booking for '{booking.skill.name}' was rescheduled by {user.name}.")
    db.commit()
    db.refresh(booking)
    return booking
