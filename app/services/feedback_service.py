from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.feedback import Feedback
from app.models.skill import Skill
from app.services.notification_helper import notify


def submit(db: Session, user, data) -> Feedback | str:
    booking = db.query(Booking).filter(Booking.id == data.booking_id).first()
    if booking is None:
        return "Booking not found"
    if booking.status != "completed":
        return "Feedback is only allowed after the session is completed"

    tutor_id = booking.skill.tutor_id
    if user.id == booking.learner_id:
        given_to = tutor_id
    elif user.id == tutor_id:
        given_to = booking.learner_id
    else:
        return "Only the learner or the tutor of this booking can leave feedback"

    feedback = Feedback(
        booking_id=booking.id,
        given_by=user.id,
        given_to=given_to,
        rating=data.rating,
        comments=data.comments,
    )
    db.add(feedback)
    try:
        notify(db, given_to, f"{user.name} left you a {data.rating}-star review.")
        db.commit()
    except IntegrityError:
        db.rollback()
        return "You have already reviewed this session"
    db.refresh(feedback)
    return feedback


def update(db: Session, feedback_id: int, user, data) -> Feedback | str:
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if feedback is None:
        return "Feedback not found"
    if feedback.given_by != user.id:
        return "You can only edit your own feedback"

    if data.rating is not None:
        feedback.rating = data.rating
    if data.comments is not None:
        feedback.comments = data.comments
    db.commit()
    db.refresh(feedback)
    return feedback


def pending_for_user(db: Session, user_id: int):
    completed = (
        db.query(Booking)
        .join(Skill, Booking.skill_id == Skill.id)
        .filter(Booking.status == "completed")
        .filter((Booking.learner_id == user_id) | (Skill.tutor_id == user_id))
        .all()
    )
    reviewed_ids = {
        f.booking_id
        for f in db.query(Feedback).filter(Feedback.given_by == user_id).all()
    }
    return [b for b in completed if b.id not in reviewed_ids]
