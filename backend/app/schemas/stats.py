from datetime import date

from pydantic import BaseModel


class DailyStats(BaseModel):
    date: date
    calories_consumed: float = 0
    calories_burned: float = 0
    calorie_balance: float = 0
    calorie_target: int = 0
    protein_g: float = 0
    fat_g: float = 0
    carbs_g: float = 0
    meal_count: int = 0
    exercise_count: int = 0
    exercise_minutes: int = 0
    sleep_duration_minutes: int | None = None
    sleep_quality: int | None = None
    weight_kg: float | None = None


class WeeklyStats(BaseModel):
    week_start: date
    week_end: date
    avg_calories_consumed: float = 0
    avg_calories_burned: float = 0
    total_exercise_minutes: int = 0
    avg_sleep_minutes: float | None = None
    weight_change: float | None = None
    daily_stats: list[DailyStats] = []


class TrendPoint(BaseModel):
    date: date
    value: float


class TrendData(BaseModel):
    points: list[TrendPoint] = []
    average: float | None = None
    min_value: float | None = None
    max_value: float | None = None
