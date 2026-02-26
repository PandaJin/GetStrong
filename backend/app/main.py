from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.routers import ai, auth, body_metrics, diet, exercise, health_plans, sleep, stats, users

app = FastAPI(
    title="GetStrong API",
    description="GetStrong 健康助手应用后端 API",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
register_exception_handlers(app)

# Routes
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["认证"])
app.include_router(users.router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["用户"])
app.include_router(diet.router, prefix=f"{settings.API_V1_PREFIX}/diet", tags=["饮食"])
app.include_router(exercise.router, prefix=f"{settings.API_V1_PREFIX}/exercise", tags=["运动"])
app.include_router(sleep.router, prefix=f"{settings.API_V1_PREFIX}/sleep", tags=["睡眠"])
app.include_router(body_metrics.router, prefix=f"{settings.API_V1_PREFIX}/body", tags=["身体指标"])
app.include_router(ai.router, prefix=f"{settings.API_V1_PREFIX}/ai", tags=["AI服务"])
app.include_router(health_plans.router, prefix=f"{settings.API_V1_PREFIX}/plans", tags=["健康计划"])
app.include_router(stats.router, prefix=f"{settings.API_V1_PREFIX}/stats", tags=["统计"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0", "app": settings.APP_NAME}


# Serve Web UI
_static_dir = Path(__file__).resolve().parent.parent / "static"
if _static_dir.is_dir():
    @app.get("/")
    async def index():
        return FileResponse(_static_dir / "index.html")

    app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")
