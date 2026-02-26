import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.core.exceptions import ForbiddenException, NotFoundException
from app.db.database import get_db
from app.models.exercise_record import ExerciseRecord
from app.models.user import User
from app.schemas.common import ApiResponse, PaginatedResponse
from app.schemas.exercise import (
    ExerciseRecordCreate,
    ExerciseRecordResponse,
    ExerciseRecordUpdate,
)

router = APIRouter()


@router.get("/records", response_model=PaginatedResponse[ExerciseRecordResponse])
async def list_exercise_records(
    record_date: date | None = Query(None),
    exercise_type: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(ExerciseRecord).where(ExerciseRecord.user_id == current_user.id)
    if record_date:
        query = query.where(ExerciseRecord.record_date == record_date)
    if exercise_type:
        query = query.where(ExerciseRecord.exercise_type == exercise_type)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(ExerciseRecord.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    records = result.scalars().all()

    return PaginatedResponse(
        data=[ExerciseRecordResponse.model_validate(r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/records", response_model=ApiResponse[ExerciseRecordResponse])
async def create_exercise_record(
    request: ExerciseRecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = ExerciseRecord(user_id=current_user.id, **request.model_dump())
    db.add(record)
    await db.flush()
    return ApiResponse(data=ExerciseRecordResponse.model_validate(record))


@router.get("/records/{record_id}", response_model=ApiResponse[ExerciseRecordResponse])
async def get_exercise_record(
    record_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(ExerciseRecord).where(ExerciseRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundException("运动记录不存在")
    if record.user_id != current_user.id:
        raise ForbiddenException()
    return ApiResponse(data=ExerciseRecordResponse.model_validate(record))


@router.put("/records/{record_id}", response_model=ApiResponse[ExerciseRecordResponse])
async def update_exercise_record(
    record_id: uuid.UUID,
    request: ExerciseRecordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(ExerciseRecord).where(ExerciseRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundException("运动记录不存在")
    if record.user_id != current_user.id:
        raise ForbiddenException()

    for key, value in request.model_dump(exclude_unset=True).items():
        setattr(record, key, value)
    await db.flush()
    return ApiResponse(data=ExerciseRecordResponse.model_validate(record))


@router.delete("/records/{record_id}", response_model=ApiResponse)
async def delete_exercise_record(
    record_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(ExerciseRecord).where(ExerciseRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundException("运动记录不存在")
    if record.user_id != current_user.id:
        raise ForbiddenException()
    await db.delete(record)
    return ApiResponse(detail="删除成功")
