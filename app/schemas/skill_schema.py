from datetime import datetime, time
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Proficiency = Literal["beginner", "intermediate", "advanced"]


class SkillCreate(BaseModel):
    category_id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    proficiency: Proficiency
    session_duration_minutes: int = Field(default=60, ge=30, le=240)


class SkillUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    proficiency: Proficiency | None = None
    session_duration_minutes: int | None = Field(default=None, ge=30, le=240)


class AvailabilityCreate(BaseModel):
    day_of_week: int = Field(..., ge=1, le=7)
    start_time: time
    end_time: time


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None


class SkillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    proficiency: str | None
    session_duration_minutes: int
    status: str
    date_listed: datetime
