from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ComplaintCreate(BaseModel):
    subject: str = Field(..., min_length=1, max_length=150)
    message: str = Field(..., min_length=1, max_length=1000)


class ComplaintResolve(BaseModel):
    admin_response: str = Field(..., min_length=1, max_length=1000)


class ComplaintResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    submitted_by: int
    subject: str
    message: str
    status: str
    admin_response: str | None
    created_at: datetime
    resolved_at: datetime | None
