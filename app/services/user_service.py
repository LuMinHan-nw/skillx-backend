from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.feedback import Feedback
from app.models.user import User
from app.schemas.user_schema import UserUpdate
from app.utils.password_handler import hash_password


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def update_profile(db: Session, user: User, data: UserUpdate) -> User:
    if data.name is not None:
        user.name = data.name
    if data.phone is not None:
        user.phone = data.phone
    if data.bio is not None:
        user.bio = data.bio
    db.commit()
    db.refresh(user)
    return user


def set_profile_picture(db: Session, user: User, path: str) -> User:
    user.profile_picture = path
    db.commit()
    db.refresh(user)
    return user


def set_password(db: Session, user: User, new_password: str) -> User:
    user.password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user


def public_profile(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user is None or user.role != "student":
        return None

    stats = (
        db.query(func.avg(Feedback.rating), func.count(Feedback.id))
        .filter(Feedback.given_to == user_id)
        .first()
    )
    reviews = (
        db.query(Feedback)
        .filter(Feedback.given_to == user_id)
        .order_by(Feedback.submitted_at.desc())
        .limit(20)
        .all()
    )
    return user, stats[0], stats[1], reviews
