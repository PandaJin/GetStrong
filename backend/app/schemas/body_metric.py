import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field


class BodyMetricCreate(BaseModel):
    record_date: date
    weight_kg: float | None = Field(None, gt=0, lt=500)
    body_fat_pct: float | None = Field(None, ge=0, le=100)
    muscle_mass_kg: float | None = Field(None, gt=0, lt=300)
    bmi: float | None = Field(None, gt=0, lt=100)
    waist_cm: float | None = Field(None, gt=0, lt=300)
    chest_cm: float | None = Field(None, gt=0, lt=300)
    hip_cm: float | None = Field(None, gt=0, lt=300)
    notes: str | None = None


class BodyMetricUpdate(BaseModel):
    weight_kg: float | None = Field(None, gt=0, lt=500)
    body_fat_pct: float | None = Field(None, ge=0, le=100)
    muscle_mass_kg: float | None = Field(None, gt=0, lt=300)
    bmi: float | None = Field(None, gt=0, lt=100)
    waist_cm: float | None = Field(None, gt=0, lt=300)
    chest_cm: float | None = Field(None, gt=0, lt=300)
    hip_cm: float | None = Field(None, gt=0, lt=300)
    notes: str | None = None


class BodyMetricResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    record_date: date
    weight_kg: float | None = None
    body_fat_pct: float | None = None
    muscle_mass_kg: float | None = None
    bmi: float | None = None
    waist_cm: float | None = None
    chest_cm: float | None = None
    hip_cm: float | None = None
    notes: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
