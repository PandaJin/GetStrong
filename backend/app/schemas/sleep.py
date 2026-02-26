import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field


class SleepRecordCreate(BaseModel):
    record_date: date
    sleep_start: datetime
    sleep_end: datetime
    quality: int | None = Field(None, ge=1, le=5)
    notes: str | None = None


class SleepRecordUpdate(BaseModel):
    sleep_start: datetime | None = None
    sleep_end: datetime | None = None
    quality: int | None = Field(None, ge=1, le=5)
    notes: str | None = None


class SleepRecordResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    record_date: date
    sleep_start: datetime
    sleep_end: datetime
    duration_minutes: int | None = None
    quality: int | None = None
    notes: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
