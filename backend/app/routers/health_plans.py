import uuid
from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.core.exceptions import AIServiceException, NotFoundException
from app.db.database import get_db
from app.models.health_plan import HealthPlan
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.health_plan import GeneratePlanRequest, HealthPlanResponse
from app.services.ai import ai_manager
from app.utils.nutrition import calculate_age, calculate_bmr, calculate_tdee

router = APIRouter()


@router.post("/generate", response_model=ApiResponse[HealthPlanResponse])
async def generate_plan(
    request: GeneratePlanRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Validate user has necessary profile data
    if not current_user.height_cm or not current_user.current_weight_kg:
        raise AIServiceException("请先在个人中心完善身高和体重信息")

    # Calculate BMR and TDEE
    age = calculate_age(current_user.birthday) if current_user.birthday else 25
    bmr = calculate_bmr(
        float(current_user.current_weight_kg),
        float(current_user.height_cm),
        age,
        current_user.gender or 1,
    )
    tdee = calculate_tdee(bmr, current_user.activity_level or "moderate")

    user_profile = {
        "nickname": current_user.nickname,
        "gender": "男" if current_user.gender == 1 else "女",
        "age": age,
        "height_cm": float(current_user.height_cm),
        "weight_kg": float(current_user.current_weight_kg),
        "target_weight_kg": float(current_user.target_weight_kg or current_user.current_weight_kg),
        "bmr": round(bmr),
        "tdee": round(tdee),
        "goal": request.goal_type,
        "activity_level": current_user.activity_level or "moderate",
        "duration_weeks": request.duration_weeks,
    }

    health_data = {
        "note": "暂无历史健康数据，请基于用户基本信息生成计划",
    }

    try:
        provider_name = ai_manager.get_provider_name(current_user.ai_provider)
        provider = ai_manager.get_provider(current_user.ai_provider)
        result = await provider.generate_health_plan(user_profile, health_data)

        # Deactivate previous plans
        prev_plans = await db.execute(
            select(HealthPlan)
            .where(HealthPlan.user_id == current_user.id)
            .where(HealthPlan.is_active == True)
        )
        for plan in prev_plans.scalars().all():
            plan.is_active = False

        # Create new plan
        today = date.today()
        plan = HealthPlan(
            user_id=current_user.id,
            goal_type=request.goal_type,
            daily_calorie_target=result.daily_calorie_target,
            daily_protein_target=round(result.daily_protein_g),
            daily_fat_target=round(result.daily_fat_g),
            daily_carbs_target=round(result.daily_carbs_g),
            daily_exercise_minutes=result.daily_exercise_minutes,
            calorie_deficit=result.calorie_deficit,
            plan_details=result.model_dump(),
            ai_provider=provider_name,
            start_date=today,
            end_date=today + timedelta(weeks=request.duration_weeks),
            duration_weeks=request.duration_weeks,
        )
        db.add(plan)

        # Update user's daily calorie target
        current_user.daily_calorie_target = result.daily_calorie_target
        current_user.fitness_goal = request.goal_type

        await db.flush()
        return ApiResponse(data=HealthPlanResponse.model_validate(plan))

    except Exception as e:
        raise AIServiceException(f"生成健康计划失败：{str(e)}")


@router.get("/", response_model=ApiResponse[list[HealthPlanResponse]])
async def list_plans(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(HealthPlan)
        .where(HealthPlan.user_id == current_user.id)
        .order_by(HealthPlan.created_at.desc())
    )
    plans = result.scalars().all()
    return ApiResponse(data=[HealthPlanResponse.model_validate(p) for p in plans])


@router.get("/active", response_model=ApiResponse[HealthPlanResponse | None])
async def get_active_plan(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(HealthPlan)
        .where(HealthPlan.user_id == current_user.id)
        .where(HealthPlan.is_active == True)
        .order_by(HealthPlan.created_at.desc())
        .limit(1)
    )
    plan = result.scalar_one_or_none()
    data = HealthPlanResponse.model_validate(plan) if plan else None
    return ApiResponse(data=data)


@router.get("/{plan_id}", response_model=ApiResponse[HealthPlanResponse])
async def get_plan(
    plan_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(HealthPlan).where(HealthPlan.id == plan_id))
    plan = result.scalar_one_or_none()
    if not plan or plan.user_id != current_user.id:
        raise NotFoundException("健康计划不存在")
    return ApiResponse(data=HealthPlanResponse.model_validate(plan))
