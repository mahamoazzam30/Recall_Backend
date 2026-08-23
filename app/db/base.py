"""Aggregates all models under one import so Alembic's autogenerate can
discover the full schema via Base.metadata. Import this module (not
`app.db.base_class`) when you need every table registered — e.g. in
alembic/env.py. Individual model files import `Base` from `base_class`
directly to avoid a circular import back through this module.
"""
from app.db.base_class import Base

from app.db.models.user import User  # noqa: E402,F401
from app.db.models.course import Course  # noqa: E402,F401
from app.db.models.course_member import CourseMember  # noqa: E402,F401
from app.db.models.module import Module  # noqa: E402,F401
from app.db.models.material import Material  # noqa: E402,F401
from app.db.models.chunk import Chunk  # noqa: E402,F401
from app.db.models.concept import Concept  # noqa: E402,F401
from app.db.models.question import Question  # noqa: E402,F401
from app.db.models.attempt import Attempt  # noqa: E402,F401
from app.db.models.mastery import Mastery  # noqa: E402,F401
from app.db.models.schedule_item import ScheduleItem  # noqa: E402,F401
from app.db.models.contest import Contest  # noqa: E402,F401
from app.db.models.exam_plan import ExamPlan, ExamPlanDay  # noqa: E402,F401
