import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, UUIDMixin


class AIRecognitionLog(Base, UUIDMixin):
    __tablename__ = "ai_recognition_logs"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    recognition_type: Mapped[str] = mapped_column(String(20))  # food / exercise
    image_url: Mapped[str] = mapped_column(String(500))
    ai_provider: Mapped[str] = mapped_column(String(20))
    request_prompt: Mapped[str | None] = mapped_column(Text)
    response_raw: Mapped[dict | None] = mapped_column(JSONB)
    parsed_result: Mapped[dict | None] = mapped_column(JSONB)
    is_accepted: Mapped[bool | None] = mapped_column(Boolean)
    linked_record_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    processing_time_ms: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
