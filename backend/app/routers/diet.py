import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.core.exceptions import ForbiddenException, NotFoundException
from app.db.database import get_db
from app.models.diet_record import DietRecord
from app.models.user import User
from app.schemas.common import ApiResponse, PaginatedResponse
from app.schemas.diet import (
    DailySummary,
    DietRecordCreate,
    DietRecordResponse,
    DietRecordUpdate,
)

router = APIRouter()


@router.get("/records", response_model=PaginatedResponse[DietRecordResponse])
async def list_diet_records(
    record_date: date | None = Query(None, description="按日期筛选"),
    meal_type: str | None = Query(None, description="按餐次筛选"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(DietRecord).where(DietRecord.user_id == current_user.id)

    if record_date:
        query = query.where(DietRecord.record_date == record_date)
    if meal_type:
        query = query.where(DietRecord.meal_type == meal_type)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Fetch paginated results
    query = query.order_by(DietRecord.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    records = result.scalars().all()

    return PaginatedResponse(
        data=[DietRecordResponse.model_validate(r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/records", response_model=ApiResponse[DietRecordResponse])
async def create_diet_record(
    request: DietRecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = DietRecord(
        user_id=current_user.id,
        **request.model_dump(),
    )
    db.add(record)
    await db.flush()
    return ApiResponse(data=DietRecordResponse.model_validate(record))


@router.get("/records/{record_id}", response_model=ApiResponse[DietRecordResponse])
async def get_diet_record(
    record_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(DietRecord).where(DietRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundException("饮食记录不存在")
    if record.user_id != current_user.id:
        raise ForbiddenException()
    return ApiResponse(data=DietRecordResponse.model_validate(record))


@router.put("/records/{record_id}", response_model=ApiResponse[DietRecordResponse])
async def update_diet_record(
    record_id: uuid.UUID,
    request: DietRecordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(DietRecord).where(DietRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundException("饮食记录不存在")
    if record.user_id != current_user.id:
        raise ForbiddenException()

    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(record, key, value)
    await db.flush()
    return ApiResponse(data=DietRecordResponse.model_validate(record))


@router.delete("/records/{record_id}", response_model=ApiResponse)
async def delete_diet_record(
    record_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(DietRecord).where(DietRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundException("饮食记录不存在")
    if record.user_id != current_user.id:
        raise ForbiddenException()

    await db.delete(record)
    return ApiResponse(detail="删除成功")


@router.get("/daily-summary", response_model=ApiResponse[DailySummary])
async def get_daily_summary(
    record_date: date = Query(..., description="日期"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(DietRecord)
        .where(DietRecord.user_id == current_user.id)
        .where(DietRecord.record_date == record_date)
        .order_by(DietRecord.created_at)
    )
    records = result.scalars().all()

    # Group by meal type
    meals: dict[str, list[DietRecordResponse]] = {}
    total_cal = total_protein = total_fat = total_carbs = 0.0

    for r in records:
        resp = DietRecordResponse.model_validate(r)
        meals.setdefault(r.meal_type, []).append(resp)
        total_cal += float(r.calories or 0)
        total_protein += float(r.protein_g or 0)
        total_fat += float(r.fat_g or 0)
        total_carbs += float(r.carbs_g or 0)

    return ApiResponse(
        data=DailySummary(
            date=record_date,
            total_calories=total_cal,
            total_protein_g=total_protein,
            total_fat_g=total_fat,
            total_carbs_g=total_carbs,
            meal_count=len(records),
            meals=meals,
        )
    )
