from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "GetStrong"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/getstrong"

    # AI Services - Kimi (Moonshot)
    KIMI_API_KEY: str = ""
    KIMI_BASE_URL: str = "https://api.moonshot.ai/v1"
    KIMI_MODEL: str = "moonshot-v1-128k-vision"

    # AI Services - Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # Alibaba Cloud OSS
    OSS_ACCESS_KEY_ID: str = ""
    OSS_ACCESS_KEY_SECRET: str = ""
    OSS_ENDPOINT: str = "oss-cn-shanghai.aliyuncs.com"
    OSS_BUCKET_NAME: str = "getstrong-images"
    OSS_CDN_DOMAIN: str = ""
    OSS_STS_ROLE_ARN: str = ""

    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
