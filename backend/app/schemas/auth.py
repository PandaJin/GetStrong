from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    phone: str = Field(..., min_length=11, max_length=20, description="手机号")
    password: str = Field(..., min_length=6, max_length=128, description="密码")
    nickname: str = Field(default="", max_length=50, description="昵称")


class LoginRequest(BaseModel):
    phone: str = Field(..., description="手机号")
    password: str = Field(..., description="密码")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str
