import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field


class ExerciseRecordCreate(BaseModel):
    record_date: date
    exercise_type: str = Field(..., max_length=50)
    exercise_name: str | None = Field(None, max_length=200)
    description: str | None = None
    duration_minutes: int | None = Field(None, ge=0)
    calories_burned: float | None = Field(None, ge=0)
    intensity: str | None = Field(None, pattern="^(low|medium|high)$")
    distance_km: float | None = Field(None, ge=0)
    heart_rate_avg: int | None = Field(None, ge=0)
    sets: int | None = Field(None, ge=0)
    reps: int | None = Field(None, ge=0)
    image_url: str | None = None
    notes: str | None = None
    source: str = "manual"


class ExerciseRecordUpdate(BaseModel):
    exercise_type: str | None = Field(None, max_length=50)
    exercise_name: str | None = Field(None, max_length=200)
    description: str | None = None
    duration_minutes: int | None = Field(None, ge=0)
    calories_burned: float | None = Field(None, ge=0)
    intensity: str | None = None
    distance_km: float | None = Field(None, ge=0)
    sets: int | None = Field(None, ge=0)
    reps: int | None = Field(None, ge=0)
    notes: str | None = None


class ExerciseRecordResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    record_date: date
    exercise_type: str
    exercise_name: str | None = None
    description: str | None = None
    duration_minutes: int | None = None
    calories_burned: float | None = None
    intensity: str | None = None
    distance_km: float | None = None
    heart_rate_avg: int | None = None
    sets: int | None = None
    reps: int | None = None
    image_url: str | None = None
    ai_analysis: dict | None = None
    source: str
    notes: str | None = None
    created_at: datetime
    image_urls: list[str] = []

    model_config = {"from_attributes": True}
