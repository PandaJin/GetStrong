import uuid
from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class HealthPlan(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "health_plans"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    goal_type: Mapped[str] = mapped_column(String(20))  # lose_weight / gain_muscle / maintain
    daily_calorie_target: Mapped[int | None] = mapped_column(Integer)
    daily_protein_target: Mapped[int | None] = mapped_column(Integer)
    daily_fat_target: Mapped[int | None] = mapped_column(Integer)
    daily_carbs_target: Mapped[int | None] = mapped_column(Integer)
    daily_exercise_minutes: Mapped[int | None] = mapped_column(Integer)
    calorie_deficit: Mapped[int | None] = mapped_column(Integer)
    plan_details: Mapped[dict] = mapped_column(JSONB, default=dict)
    ai_provider: Mapped[str | None] = mapped_column(String(20))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    duration_weeks: Mapped[int] = mapped_column(Integer, default=4)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="health_plans")
