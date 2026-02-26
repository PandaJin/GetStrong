import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field


class DietRecordCreate(BaseModel):
    record_date: date
    meal_type: str = Field(..., pattern="^(breakfast|lunch|dinner|snack)$")
    food_name: str = Field(..., max_length=200)
    description: str | None = None
    calories: float | None = Field(None, ge=0)
    protein_g: float | None = Field(None, ge=0)
    fat_g: float | None = Field(None, ge=0)
    carbs_g: float | None = Field(None, ge=0)
    fiber_g: float | None = Field(None, ge=0)
    serving_size: str | None = None
    image_url: str | None = None
    source: str = "manual"


class DietRecordUpdate(BaseModel):
    meal_type: str | None = None
    food_name: str | None = Field(None, max_length=200)
    description: str | None = None
    calories: float | None = Field(None, ge=0)
    protein_g: float | None = Field(None, ge=0)
    fat_g: float | None = Field(None, ge=0)
    carbs_g: float | None = Field(None, ge=0)
    fiber_g: float | None = Field(None, ge=0)
    serving_size: str | None = None


class DietRecordResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    record_date: date
    meal_type: str
    food_name: str
    description: str | None = None
    calories: float | None = None
    protein_g: float | None = None
    fat_g: float | None = None
    carbs_g: float | None = None
    fiber_g: float | None = None
    serving_size: str | None = None
    image_url: str | None = None
    ai_analysis: dict | None = None
    source: str
    created_at: datetime
    image_urls: list[str] = []

    model_config = {"from_attributes": True}


class DailySummary(BaseModel):
    date: date
    total_calories: float = 0
    total_protein_g: float = 0
    total_fat_g: float = 0
    total_carbs_g: float = 0
    meal_count: int = 0
    meals: dict[str, list[DietRecordResponse]] = {}  # grouped by meal_type
