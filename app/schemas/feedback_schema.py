from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FeedbackCreate(BaseModel):
    booking_id: int
    rating: int = Field(..., ge=1, le=5)
    comments: str | None = Field(default=None, max_length=500)


class FeedbackUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    comments: str | None = Field(default=None, max_length=500)


class FeedbackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    booking_id: int
    given_by: int
    given_to: int
    rating: int
    comments: str | None
    submitted_at: datetime
