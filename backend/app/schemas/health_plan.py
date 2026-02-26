import uuid
from datetime import date, datetime

from pydantic import BaseModel


class GeneratePlanRequest(BaseModel):
    goal_type: str  # lose_weight / gain_muscle / maintain
    duration_weeks: int = 4


class HealthPlanResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    goal_type: str
    daily_calorie_target: int | None = None
    daily_protein_target: int | None = None
    daily_fat_target: int | None = None
    daily_carbs_target: int | None = None
    daily_exercise_minutes: int | None = None
    calorie_deficit: int | None = None
    plan_details: dict
    ai_provider: str | None = None
    start_date: date
    end_date: date
    duration_weeks: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
