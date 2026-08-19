"""Course access control.

A course is visible to its owner and to anyone who has joined it as a
study-group member (see CourseMember). Every route that scopes a resource
to "the current user's course" should go through get_accessible_course
instead of comparing course.user_id directly, so shared courses behave
consistently everywhere.
"""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.course import Course
from app.db.models.course_member import CourseMember


def can_access_course(db: Session, course: Course, user_id: uuid.UUID) -> bool:
    if course.user_id == user_id:
        return True
    stmt = select(CourseMember.id).where(CourseMember.course_id == course.id, CourseMember.user_id == user_id)
    return db.execute(stmt).first() is not None


def get_accessible_course(db: Session, course_id: uuid.UUID, user_id: uuid.UUID) -> Course | None:
    course = db.get(Course, course_id)
    if course is None or not can_access_course(db, course, user_id):
        return None
    return course
