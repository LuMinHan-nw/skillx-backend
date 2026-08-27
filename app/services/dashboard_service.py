from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.certificate import Certificate
from app.models.feedback import Feedback
from app.models.skill import Skill, SkillCategory
from app.models.user import User


def summary(db: Session):
    return {
        "total_students": db.query(func.count(User.id))
        .filter(User.role == "student")
        .scalar(),
        "total_skills": db.query(func.count(Skill.id)).scalar(),
        "pending_skills": db.query(func.count(Skill.id))
        .filter(Skill.status == "pending")
        .scalar(),
        "total_bookings": db.query(func.count(Booking.id)).scalar(),
        "completed_sessions": db.query(func.count(Booking.id))
        .filter(Booking.status == "completed")
        .scalar(),
        "certificates_issued": db.query(func.count(Certificate.id)).scalar(),
    }


def top_skills(db: Session, limit: int = 5):
    rows = (
        db.query(Skill.name, func.count(Booking.id).label("bookings"))
        .join(Booking, Booking.skill_id == Skill.id)
        .group_by(Skill.id, Skill.name)
        .order_by(func.count(Booking.id).desc())
        .limit(limit)
        .all()
    )
    return [{"skill": r[0], "bookings": r[1]} for r in rows]


def top_students(db: Session, limit: int = 5):
    rows = (
        db.query(
            User.name,
            func.avg(Feedback.rating).label("avg_rating"),
            func.count(Feedback.id).label("reviews"),
        )
        .join(Feedback, Feedback.given_to == User.id)
        .group_by(User.id, User.name)
        .order_by(func.avg(Feedback.rating).desc(), func.count(Feedback.id).desc())
        .limit(limit)
        .all()
    )
    return [
        {"student": r[0], "avg_rating": round(float(r[1]), 2), "reviews": r[2]}
        for r in rows
    ]


def exchanges_weekly(db: Session):
    # "%x-%v" is MySQL's ISO year + ISO week number, e.g. "2026-31".
    week = func.date_format(Booking.session_date, "%x-%v")
    rows = (
        db.query(week.label("week"), func.count(Booking.id))
        .filter(Booking.status == "completed")
        .group_by("week")
        .order_by("week")
        .all()
    )
    return [{"week": r[0], "completed": r[1]} for r in rows]


# A rating is stored against a booking, not against a category, so the category
# has to be reached through three joins: category -> skill -> booking -> feedback.
def rating_by_category(db: Session):
    rows = (
        db.query(
            SkillCategory.name,
            func.avg(Feedback.rating).label("avg_rating"),
            func.count(Feedback.id).label("reviews"),
        )
        .join(Skill, Skill.category_id == SkillCategory.id)
        .join(Booking, Booking.skill_id == Skill.id)
        .join(Feedback, Feedback.booking_id == Booking.id)
        .group_by(SkillCategory.id, SkillCategory.name)
        .order_by(func.avg(Feedback.rating).desc())
        .all()
    )
    return [
        {"category": r[0], "avg_rating": round(float(r[1]), 2), "reviews": r[2]}
        for r in rows
    ]
