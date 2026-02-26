import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, Numeric, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    phone: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    nickname: Mapped[str] = mapped_column(String(50), default="")
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    gender: Mapped[int] = mapped_column(SmallInteger, default=0)  # 0=unknown 1=male 2=female
    birthday: Mapped[date | None] = mapped_column(Date)
    height_cm: Mapped[float | None] = mapped_column(Numeric(5, 1))
    current_weight_kg: Mapped[float | None] = mapped_column(Numeric(5, 1))
    target_weight_kg: Mapped[float | None] = mapped_column(Numeric(5, 1))
    fitness_goal: Mapped[str | None] = mapped_column(String(20))  # lose_weight / gain_muscle / maintain / improve_health
    activity_level: Mapped[str | None] = mapped_column(String(20))  # sedentary / light / moderate / active / very_active
    ai_provider: Mapped[str] = mapped_column(String(20), default="kimi")  # kimi / gemini / auto
    daily_calorie_target: Mapped[int | None] = mapped_column()
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    diet_records = relationship("DietRecord", back_populates="user", cascade="all, delete-orphan")
    exercise_records = relationship("ExerciseRecord", back_populates="user", cascade="all, delete-orphan")
    sleep_records = relationship("SleepRecord", back_populates="user", cascade="all, delete-orphan")
    body_metrics = relationship("BodyMetric", back_populates="user", cascade="all, delete-orphan")
    health_plans = relationship("HealthPlan", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
