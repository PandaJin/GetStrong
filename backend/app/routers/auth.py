from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
)
from app.schemas.common import ApiResponse
from app.schemas.user import UserResponse

router = APIRouter()


@router.post("/register", response_model=ApiResponse[TokenResponse])
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # Check if phone already exists
    result = await db.execute(select(User).where(User.phone == request.phone))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该手机号已被注册",
        )

    user = User(
        phone=request.phone,
        password_hash=get_password_hash(request.password),
        nickname=request.nickname or f"用户{request.phone[-4:]}",
    )
    db.add(user)
    await db.flush()

    token_data = TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )
    return ApiResponse(data=token_data)


@router.post("/login", response_model=ApiResponse[TokenResponse])
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.phone == request.phone))
    user = result.scalar_one_or_none()

    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="手机号或密码错误",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用",
        )

    token_data = TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )
    return ApiResponse(data=token_data)


@router.post("/refresh", response_model=ApiResponse[TokenResponse])
async def refresh_token(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    try:
        payload = decode_token(request.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="无效的刷新令牌")
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="刷新令牌已过期")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="用户不存在")

    token_data = TokenResponse(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )
    return ApiResponse(data=token_data)


@router.get("/me", response_model=ApiResponse[UserResponse])
async def get_me(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        __import__("app.core.dependencies", fromlist=["get_current_user"]).get_current_user
    ),
):
    return ApiResponse(data=UserResponse.model_validate(current_user))
