import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, Numeric, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class ExerciseRecord(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "exercise_records"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    record_date: Mapped[date] = mapped_column(Date, index=True)
    exercise_type: Mapped[str] = mapped_column(String(50))  # running / swimming / weight_training / yoga etc.
    exercise_name: Mapped[str | None] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
    calories_burned: Mapped[float | None] = mapped_column(Numeric(7, 1))
    intensity: Mapped[str | None] = mapped_column(String(20))  # low / medium / high
    distance_km: Mapped[float | None] = mapped_column(Numeric(6, 2))
    heart_rate_avg: Mapped[int | None] = mapped_column(Integer)
    sets: Mapped[int | None] = mapped_column(Integer)
    reps: Mapped[int | None] = mapped_column(Integer)
    image_url: Mapped[str | None] = mapped_column(Text)
    ai_analysis: Mapped[dict | None] = mapped_column(JSONB)
    source: Mapped[str] = mapped_column(String(20), default="manual")
    notes: Mapped[str | None] = mapped_column(Text)

    # Relationships
    user = relationship("User", back_populates="exercise_records")
    images = relationship("ExerciseRecordImage", back_populates="exercise_record", cascade="all, delete-orphan")


class ExerciseRecordImage(Base, UUIDMixin):
    __tablename__ = "exercise_record_images"

    exercise_record_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("exercise_records.id", ondelete="CASCADE"), index=True
    )
    image_url: Mapped[str] = mapped_column(String(500))
    thumbnail_url: Mapped[str | None] = mapped_column(String(500))
    sort_order: Mapped[int] = mapped_column(SmallInteger, default=0)

    exercise_record = relationship("ExerciseRecord", back_populates="images")
