"""courses (renamed from subjects), modules, exam_plans, exam_plan_days, mastery.error_note

Revision ID: 0002
Revises: 0001
Create Date: 2026-08-17

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table("subjects", "courses")
    op.add_column("courses", sa.Column("color_tag", sa.String(20), nullable=True))

    op.alter_column("materials", "subject_id", new_column_name="course_id")
    op.alter_column("concepts", "subject_id", new_column_name="course_id")

    op.create_table(
        "modules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("courses.id"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("order_index", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_modules_course_id", "modules", ["course_id"])

    op.add_column(
        "materials",
        sa.Column("module_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("modules.id"), nullable=True),
    )

    op.add_column("mastery", sa.Column("error_note", sa.Text, nullable=True))

    exam_plan_status = sa.Enum("active", "completed", "cancelled", name="exam_plan_status")
    op.create_table(
        "exam_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("courses.id"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("exam_date", sa.Date, nullable=False),
        sa.Column("status", exam_plan_status, nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_exam_plans_course_id", "exam_plans", ["course_id"])

    op.create_table(
        "exam_plan_days",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "exam_plan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exam_plans.id"), nullable=False
        ),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("target_concept_ids", postgresql.JSONB, nullable=False),
        sa.Column("completed", sa.Boolean, nullable=False, server_default="false"),
    )
    op.create_index("ix_exam_plan_days_exam_plan_id", "exam_plan_days", ["exam_plan_id"])


def downgrade() -> None:
    op.drop_table("exam_plan_days")
    op.drop_table("exam_plans")
    sa.Enum(name="exam_plan_status").drop(op.get_bind(), checkfirst=True)

    op.drop_column("mastery", "error_note")

    op.drop_column("materials", "module_id")
    op.drop_table("modules")

    op.alter_column("concepts", "course_id", new_column_name="subject_id")
    op.alter_column("materials", "course_id", new_column_name="subject_id")

    op.drop_column("courses", "color_tag")
    op.rename_table("courses", "subjects")
