"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-02-26 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # users
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("phone", sa.String(20), unique=True, index=True, nullable=True),
        sa.Column("email", sa.String(255), unique=True, index=True, nullable=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("nickname", sa.String(50), nullable=False, server_default=""),
        sa.Column("avatar_url", sa.String(500), nullable=True),
        sa.Column("gender", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("birthday", sa.Date(), nullable=True),
        sa.Column("height_cm", sa.Numeric(5, 1), nullable=True),
        sa.Column("current_weight_kg", sa.Numeric(5, 1), nullable=True),
        sa.Column("target_weight_kg", sa.Numeric(5, 1), nullable=True),
        sa.Column("fitness_goal", sa.String(20), nullable=True),
        sa.Column("activity_level", sa.String(20), nullable=True),
        sa.Column("ai_provider", sa.String(20), nullable=False, server_default="kimi"),
        sa.Column("daily_calorie_target", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # diet_records
    op.create_table(
        "diet_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("record_date", sa.Date(), nullable=False, index=True),
        sa.Column("meal_type", sa.String(20), nullable=False),
        sa.Column("food_name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("calories", sa.Numeric(7, 1), nullable=True),
        sa.Column("protein_g", sa.Numeric(6, 1), nullable=True),
        sa.Column("fat_g", sa.Numeric(6, 1), nullable=True),
        sa.Column("carbs_g", sa.Numeric(6, 1), nullable=True),
        sa.Column("fiber_g", sa.Numeric(6, 1), nullable=True),
        sa.Column("serving_size", sa.String(50), nullable=True),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("ai_analysis", postgresql.JSONB(), nullable=True),
        sa.Column("source", sa.String(20), nullable=False, server_default="manual"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # diet_record_images
    op.create_table(
        "diet_record_images",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("diet_record_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("diet_records.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("image_url", sa.String(500), nullable=False),
        sa.Column("thumbnail_url", sa.String(500), nullable=True),
        sa.Column("sort_order", sa.SmallInteger(), nullable=False, server_default="0"),
    )

    # exercise_records
    op.create_table(
        "exercise_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("record_date", sa.Date(), nullable=False, index=True),
        sa.Column("exercise_type", sa.String(50), nullable=False),
        sa.Column("exercise_name", sa.String(200), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        sa.Column("calories_burned", sa.Numeric(7, 1), nullable=True),
        sa.Column("intensity", sa.String(20), nullable=True),
        sa.Column("distance_km", sa.Numeric(6, 2), nullable=True),
        sa.Column("heart_rate_avg", sa.Integer(), nullable=True),
        sa.Column("sets", sa.Integer(), nullable=True),
        sa.Column("reps", sa.Integer(), nullable=True),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("ai_analysis", postgresql.JSONB(), nullable=True),
        sa.Column("source", sa.String(20), nullable=False, server_default="manual"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # exercise_record_images
    op.create_table(
        "exercise_record_images",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("exercise_record_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exercise_records.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("image_url", sa.String(500), nullable=False),
        sa.Column("thumbnail_url", sa.String(500), nullable=True),
        sa.Column("sort_order", sa.SmallInteger(), nullable=False, server_default="0"),
    )

    # sleep_records
    op.create_table(
        "sleep_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("record_date", sa.Date(), nullable=False, index=True),
        sa.Column("sleep_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sleep_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        sa.Column("quality", sa.SmallInteger(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # body_metrics
    op.create_table(
        "body_metrics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("record_date", sa.Date(), nullable=False, index=True),
        sa.Column("weight_kg", sa.Numeric(5, 1), nullable=True),
        sa.Column("body_fat_pct", sa.Numeric(4, 1), nullable=True),
        sa.Column("muscle_mass_kg", sa.Numeric(5, 1), nullable=True),
        sa.Column("bmi", sa.Numeric(4, 1), nullable=True),
        sa.Column("waist_cm", sa.Numeric(5, 1), nullable=True),
        sa.Column("chest_cm", sa.Numeric(5, 1), nullable=True),
        sa.Column("hip_cm", sa.Numeric(5, 1), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # health_plans
    op.create_table(
        "health_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("goal_type", sa.String(20), nullable=False),
        sa.Column("daily_calorie_target", sa.Integer(), nullable=True),
        sa.Column("daily_protein_target", sa.Integer(), nullable=True),
        sa.Column("daily_fat_target", sa.Integer(), nullable=True),
        sa.Column("daily_carbs_target", sa.Integer(), nullable=True),
        sa.Column("daily_exercise_minutes", sa.Integer(), nullable=True),
        sa.Column("calorie_deficit", sa.Integer(), nullable=True),
        sa.Column("plan_details", postgresql.JSONB(), nullable=False, server_default="{}"),
        sa.Column("ai_provider", sa.String(20), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("duration_weeks", sa.Integer(), nullable=False, server_default="4"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # chat_sessions
    op.create_table(
        "chat_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("title", sa.String(200), nullable=True),
        sa.Column("ai_provider", sa.String(20), nullable=False, server_default="kimi"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # chat_messages
    op.create_table(
        "chat_messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("image_urls", postgresql.JSONB(), nullable=True),
        sa.Column("token_count", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ai_recognition_logs
    op.create_table(
        "ai_recognition_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("recognition_type", sa.String(20), nullable=False),
        sa.Column("image_url", sa.String(500), nullable=False),
        sa.Column("ai_provider", sa.String(20), nullable=False),
        sa.Column("request_prompt", sa.Text(), nullable=True),
        sa.Column("response_raw", postgresql.JSONB(), nullable=True),
        sa.Column("parsed_result", postgresql.JSONB(), nullable=True),
        sa.Column("is_accepted", sa.Boolean(), nullable=True),
        sa.Column("linked_record_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("processing_time_ms", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("ai_recognition_logs")
    op.drop_table("chat_messages")
    op.drop_table("chat_sessions")
    op.drop_table("health_plans")
    op.drop_table("body_metrics")
    op.drop_table("sleep_records")
    op.drop_table("exercise_record_images")
    op.drop_table("exercise_records")
    op.drop_table("diet_record_images")
    op.drop_table("diet_records")
    op.drop_table("users")
