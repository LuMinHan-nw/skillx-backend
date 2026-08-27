from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


UserRole = Literal["admin", "student"]


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., max_length=150)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72)
    role: UserRole


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=20)
    bio: str | None = Field(default=None, max_length=500)


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    phone: str | None
    bio: str | None
    status: str
    created_at: datetime
