import uuid
from datetime import date, datetime

from sqlalchemy import Date, ForeignKey, Numeric, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class DietRecord(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "diet_records"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    record_date: Mapped[date] = mapped_column(Date, index=True)
    meal_type: Mapped[str] = mapped_column(String(20))  # breakfast / lunch / dinner / snack
    food_name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    calories: Mapped[float | None] = mapped_column(Numeric(7, 1))
    protein_g: Mapped[float | None] = mapped_column(Numeric(6, 1))
    fat_g: Mapped[float | None] = mapped_column(Numeric(6, 1))
    carbs_g: Mapped[float | None] = mapped_column(Numeric(6, 1))
    fiber_g: Mapped[float | None] = mapped_column(Numeric(6, 1))
    serving_size: Mapped[str | None] = mapped_column(String(50))
    image_url: Mapped[str | None] = mapped_column(Text)
    ai_analysis: Mapped[dict | None] = mapped_column(JSONB)
    source: Mapped[str] = mapped_column(String(20), default="manual")  # manual / ai_image / ai_chat

    # Relationships
    user = relationship("User", back_populates="diet_records")
    images = relationship("DietRecordImage", back_populates="diet_record", cascade="all, delete-orphan")


class DietRecordImage(Base, UUIDMixin):
    __tablename__ = "diet_record_images"

    diet_record_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("diet_records.id", ondelete="CASCADE"), index=True
    )
    image_url: Mapped[str] = mapped_column(String(500))
    thumbnail_url: Mapped[str | None] = mapped_column(String(500))
    sort_order: Mapped[int] = mapped_column(SmallInteger, default=0)

    diet_record = relationship("DietRecord", back_populates="images")
