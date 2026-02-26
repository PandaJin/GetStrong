from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.user import UserResponse, UserUpdateRequest

router = APIRouter()


@router.get("/me", response_model=ApiResponse[UserResponse])
async def get_profile(current_user: User = Depends(get_current_user)):
    return ApiResponse(data=UserResponse.model_validate(current_user))


@router.put("/me", response_model=ApiResponse[UserResponse])
async def update_profile(
    request: UserUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current_user, key, value)
    await db.flush()
    return ApiResponse(data=UserResponse.model_validate(current_user))
