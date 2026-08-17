import uuid

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.models.mixins import TimestampMixin, UUIDPKMixin


class Module(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "modules"

    course_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    course: Mapped["Course"] = relationship(back_populates="modules")
    materials: Mapped[list["Material"]] = relationship(back_populates="module")
