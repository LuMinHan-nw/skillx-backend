from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth_schema import LoginRequest, RegisterRequest
from app.schemas.user_schema import UserResponse
from app.services import auth_service
from app.utils.jwt_handler import create_access_token
from app.utils.response import success_response


def register(data: RegisterRequest, db: Session):
    user = auth_service.register_user(db, data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    token = create_access_token({"sub": str(user.id), "role": user.role})
    return success_response(
        "User registered successfully",
        {
            "access_token": token,
            "token_type": "bearer",
            "user": UserResponse.model_validate(user).model_dump(),
        },
    )


def login(data: LoginRequest, db: Session):
    user = auth_service.login_user(db, data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if user.status == "suspended":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is suspended",
        )

    token = create_access_token({"sub": str(user.id), "role": user.role})
    return success_response(
        "Login successful",
        {
            "access_token": token,
            "token_type": "bearer",
            "user": UserResponse.model_validate(user).model_dump(),
        },
    )


def me(current_user: User):
    return success_response(
        "Current user",
        UserResponse.model_validate(current_user).model_dump(),
    )
