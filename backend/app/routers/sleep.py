import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.core.exceptions import ForbiddenException, NotFoundException
from app.db.database import get_db
from app.models.sleep_record import SleepRecord
from app.models.user import User
from app.schemas.common import ApiResponse, PaginatedResponse
from app.schemas.sleep import SleepRecordCreate, SleepRecordResponse, SleepRecordUpdate

router = APIRouter()


@router.get("/records", response_model=PaginatedResponse[SleepRecordResponse])
async def list_sleep_records(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(SleepRecord).where(SleepRecord.user_id == current_user.id)
    if start_date:
        query = query.where(SleepRecord.record_date >= start_date)
    if end_date:
        query = query.where(SleepRecord.record_date <= end_date)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(SleepRecord.record_date.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    records = result.scalars().all()

    return PaginatedResponse(
        data=[SleepRecordResponse.model_validate(r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/records", response_model=ApiResponse[SleepRecordResponse])
async def create_sleep_record(
    request: SleepRecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Auto-calculate duration
    duration = int((request.sleep_end - request.sleep_start).total_seconds() / 60)

    record = SleepRecord(
        user_id=current_user.id,
        duration_minutes=duration,
        **request.model_dump(),
    )
    db.add(record)
    await db.flush()
    return ApiResponse(data=SleepRecordResponse.model_validate(record))


@router.get("/records/{record_id}", response_model=ApiResponse[SleepRecordResponse])
async def get_sleep_record(
    record_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(SleepRecord).where(SleepRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundException("睡眠记录不存在")
    if record.user_id != current_user.id:
        raise ForbiddenException()
    return ApiResponse(data=SleepRecordResponse.model_validate(record))


@router.put("/records/{record_id}", response_model=ApiResponse[SleepRecordResponse])
async def update_sleep_record(
    record_id: uuid.UUID,
    request: SleepRecordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(SleepRecord).where(SleepRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundException("睡眠记录不存在")
    if record.user_id != current_user.id:
        raise ForbiddenException()

    for key, value in request.model_dump(exclude_unset=True).items():
        setattr(record, key, value)

    if request.sleep_start or request.sleep_end:
        start = request.sleep_start or record.sleep_start
        end = request.sleep_end or record.sleep_end
        record.duration_minutes = int((end - start).total_seconds() / 60)

    await db.flush()
    return ApiResponse(data=SleepRecordResponse.model_validate(record))


@router.delete("/records/{record_id}", response_model=ApiResponse)
async def delete_sleep_record(
    record_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(SleepRecord).where(SleepRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundException("睡眠记录不存在")
    if record.user_id != current_user.id:
        raise ForbiddenException()
    await db.delete(record)
    return ApiResponse(detail="删除成功")
