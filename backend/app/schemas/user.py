import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: uuid.UUID
    phone: str | None = None
    nickname: str
    avatar_url: str | None = None
    gender: int = 0
    birthday: date | None = None
    height_cm: float | None = None
    current_weight_kg: float | None = None
    target_weight_kg: float | None = None
    fitness_goal: str | None = None
    activity_level: str | None = None
    ai_provider: str = "kimi"
    daily_calorie_target: int | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdateRequest(BaseModel):
    nickname: str | None = Field(None, max_length=50)
    gender: int | None = Field(None, ge=0, le=2)
    birthday: date | None = None
    height_cm: float | None = Field(None, gt=0, lt=300)
    current_weight_kg: float | None = Field(None, gt=0, lt=500)
    target_weight_kg: float | None = Field(None, gt=0, lt=500)
    fitness_goal: str | None = None
    activity_level: str | None = None
    ai_provider: str | None = None
