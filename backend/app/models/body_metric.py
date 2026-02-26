import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class BodyMetric(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "body_metrics"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    record_date: Mapped[date] = mapped_column(Date, index=True)
    weight_kg: Mapped[float | None] = mapped_column(Numeric(5, 1))
    body_fat_pct: Mapped[float | None] = mapped_column(Numeric(4, 1))
    muscle_mass_kg: Mapped[float | None] = mapped_column(Numeric(5, 1))
    bmi: Mapped[float | None] = mapped_column(Numeric(4, 1))
    waist_cm: Mapped[float | None] = mapped_column(Numeric(5, 1))
    chest_cm: Mapped[float | None] = mapped_column(Numeric(5, 1))
    hip_cm: Mapped[float | None] = mapped_column(Numeric(5, 1))
    notes: Mapped[str | None] = mapped_column(Text)

    # Relationships
    user = relationship("User", back_populates="body_metrics")
