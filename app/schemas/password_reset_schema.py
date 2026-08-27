from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class PasswordResetRequestCreate(BaseModel):
    email: EmailStr = Field(..., max_length=150)


class PasswordResetComplete(BaseModel):
    email: EmailStr = Field(..., max_length=150)
    new_password: str = Field(..., min_length=6, max_length=72)


class PasswordResetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: str
    requested_at: datetime
    approved_at: datetime | None
    completed_at: datetime | None
