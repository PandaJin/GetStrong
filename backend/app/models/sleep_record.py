import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, SmallInteger, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class SleepRecord(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "sleep_records"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    record_date: Mapped[date] = mapped_column(Date, index=True)
    sleep_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    sleep_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
    quality: Mapped[int | None] = mapped_column(SmallInteger)  # 1-5
    notes: Mapped[str | None] = mapped_column(Text)

    # Relationships
    user = relationship("User", back_populates="sleep_records")
