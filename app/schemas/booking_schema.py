from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, Field, model_validator


class BookingCreate(BaseModel):
    skill_id: int
    session_date: date
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def check_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class BookingReschedule(BaseModel):
    session_date: date
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def check_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class BookingCancel(BaseModel):
    reason: str | None = Field(default=None, max_length=255)


class BookingMeetingLink(BaseModel):
    meeting_link: str = Field(..., min_length=1, max_length=500)


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    skill_id: int
    learner_id: int
    session_date: date
    start_time: time
    end_time: time
    status: str
    cancel_reason: str | None
    meeting_link: str | None
    booked_at: datetime
