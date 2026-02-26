from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.body_metric import BodyMetric
from app.models.diet_record import DietRecord
from app.models.exercise_record import ExerciseRecord
from app.models.sleep_record import SleepRecord
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.stats import DailyStats, TrendData, TrendPoint, WeeklyStats

router = APIRouter()


@router.get("/daily", response_model=ApiResponse[DailyStats])
async def get_daily_stats(
    target_date: date = Query(default_factory=date.today, alias="date"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Diet stats
    diet_result = await db.execute(
        select(
            func.coalesce(func.sum(DietRecord.calories), 0).label("total_cal"),
            func.coalesce(func.sum(DietRecord.protein_g), 0).label("total_protein"),
            func.coalesce(func.sum(DietRecord.fat_g), 0).label("total_fat"),
            func.coalesce(func.sum(DietRecord.carbs_g), 0).label("total_carbs"),
            func.count(DietRecord.id).label("meal_count"),
        )
        .where(DietRecord.user_id == current_user.id)
        .where(DietRecord.record_date == target_date)
    )
    diet_row = diet_result.one()

    # Exercise stats
    exercise_result = await db.execute(
        select(
            func.coalesce(func.sum(ExerciseRecord.calories_burned), 0).label("total_burned"),
            func.coalesce(func.sum(ExerciseRecord.duration_minutes), 0).label("total_min"),
            func.count(ExerciseRecord.id).label("exercise_count"),
        )
        .where(ExerciseRecord.user_id == current_user.id)
        .where(ExerciseRecord.record_date == target_date)
    )
    exercise_row = exercise_result.one()

    # Sleep stats
    sleep_result = await db.execute(
        select(SleepRecord)
        .where(SleepRecord.user_id == current_user.id)
        .where(SleepRecord.record_date == target_date)
        .limit(1)
    )
    sleep = sleep_result.scalar_one_or_none()

    # Latest weight
    weight_result = await db.execute(
        select(BodyMetric.weight_kg)
        .where(BodyMetric.user_id == current_user.id)
        .where(BodyMetric.record_date <= target_date)
        .order_by(BodyMetric.record_date.desc())
        .limit(1)
    )
    weight = weight_result.scalar_one_or_none()

    calories_consumed = float(diet_row.total_cal)
    calories_burned = float(exercise_row.total_burned)

    return ApiResponse(
        data=DailyStats(
            date=target_date,
            calories_consumed=calories_consumed,
            calories_burned=calories_burned,
            calorie_balance=calories_consumed - calories_burned,
            calorie_target=current_user.daily_calorie_target or 2000,
            protein_g=float(diet_row.total_protein),
            fat_g=float(diet_row.total_fat),
            carbs_g=float(diet_row.total_carbs),
            meal_count=diet_row.meal_count,
            exercise_count=exercise_row.exercise_count,
            exercise_minutes=int(exercise_row.total_min),
            sleep_duration_minutes=sleep.duration_minutes if sleep else None,
            sleep_quality=sleep.quality if sleep else None,
            weight_kg=float(weight) if weight else None,
        )
    )


@router.get("/weight-trend", response_model=ApiResponse[TrendData])
async def get_weight_trend(
    days: int = Query(30, ge=7, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    start_date = date.today() - timedelta(days=days)
    result = await db.execute(
        select(BodyMetric.record_date, BodyMetric.weight_kg)
        .where(BodyMetric.user_id == current_user.id)
        .where(BodyMetric.record_date >= start_date)
        .where(BodyMetric.weight_kg.is_not(None))
        .order_by(BodyMetric.record_date)
    )
    rows = result.all()
    points = [TrendPoint(date=r.record_date, value=float(r.weight_kg)) for r in rows]
    values = [p.value for p in points]

    return ApiResponse(
        data=TrendData(
            points=points,
            average=round(sum(values) / len(values), 1) if values else None,
            min_value=min(values) if values else None,
            max_value=max(values) if values else None,
        )
    )


@router.get("/calorie-trend", response_model=ApiResponse[TrendData])
async def get_calorie_trend(
    days: int = Query(30, ge=7, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    start_date = date.today() - timedelta(days=days)
    result = await db.execute(
        select(
            DietRecord.record_date,
            func.sum(DietRecord.calories).label("total"),
        )
        .where(DietRecord.user_id == current_user.id)
        .where(DietRecord.record_date >= start_date)
        .group_by(DietRecord.record_date)
        .order_by(DietRecord.record_date)
    )
    rows = result.all()
    points = [TrendPoint(date=r.record_date, value=float(r.total or 0)) for r in rows]
    values = [p.value for p in points]

    return ApiResponse(
        data=TrendData(
            points=points,
            average=round(sum(values) / len(values), 1) if values else None,
            min_value=min(values) if values else None,
            max_value=max(values) if values else None,
        )
    )
