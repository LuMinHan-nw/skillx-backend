from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth_schema import LoginRequest, RegisterRequest
from app.utils.password_handler import hash_password, verify_password


def register_user(db: Session, data: RegisterRequest) -> User | None:
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        return None

    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        phone=data.phone,
        role="student",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, data: LoginRequest) -> User | None:
    user = db.query(User).filter(User.email == data.email).first()
    if user is None:
        return None

    if not verify_password(data.password, user.password):
        return None

    return user
