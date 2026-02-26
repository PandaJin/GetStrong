import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.core.exceptions import ForbiddenException, NotFoundException
from app.db.database import get_db
from app.models.body_metric import BodyMetric
from app.models.user import User
from app.schemas.body_metric import BodyMetricCreate, BodyMetricResponse, BodyMetricUpdate
from app.schemas.common import ApiResponse, PaginatedResponse

router = APIRouter()


@router.get("/metrics", response_model=PaginatedResponse[BodyMetricResponse])
async def list_body_metrics(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(BodyMetric).where(BodyMetric.user_id == current_user.id)
    if start_date:
        query = query.where(BodyMetric.record_date >= start_date)
    if end_date:
        query = query.where(BodyMetric.record_date <= end_date)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(BodyMetric.record_date.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    records = result.scalars().all()

    return PaginatedResponse(
        data=[BodyMetricResponse.model_validate(r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/metrics", response_model=ApiResponse[BodyMetricResponse])
async def create_body_metric(
    request: BodyMetricCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = BodyMetric(user_id=current_user.id, **request.model_dump())
    db.add(record)
    await db.flush()

    # Update user's current weight if provided
    if request.weight_kg:
        current_user.current_weight_kg = request.weight_kg

    return ApiResponse(data=BodyMetricResponse.model_validate(record))


@router.get("/metrics/latest", response_model=ApiResponse[BodyMetricResponse | None])
async def get_latest_body_metric(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(BodyMetric)
        .where(BodyMetric.user_id == current_user.id)
        .order_by(BodyMetric.record_date.desc())
        .limit(1)
    )
    record = result.scalar_one_or_none()
    data = BodyMetricResponse.model_validate(record) if record else None
    return ApiResponse(data=data)


@router.put("/metrics/{record_id}", response_model=ApiResponse[BodyMetricResponse])
async def update_body_metric(
    record_id: uuid.UUID,
    request: BodyMetricUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(BodyMetric).where(BodyMetric.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundException("身体指标记录不存在")
    if record.user_id != current_user.id:
        raise ForbiddenException()

    for key, value in request.model_dump(exclude_unset=True).items():
        setattr(record, key, value)
    await db.flush()
    return ApiResponse(data=BodyMetricResponse.model_validate(record))


@router.delete("/metrics/{record_id}", response_model=ApiResponse)
async def delete_body_metric(
    record_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(BodyMetric).where(BodyMetric.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise NotFoundException("身体指标记录不存在")
    if record.user_id != current_user.id:
        raise ForbiddenException()
    await db.delete(record)
    return ApiResponse(detail="删除成功")
