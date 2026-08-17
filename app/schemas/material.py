import uuid

from pydantic import BaseModel

from app.db.models.material import MaterialStatus, SourceType


class MaterialResponse(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    module_id: uuid.UUID | None = None
    filename: str
    source_type: SourceType
    status: MaterialStatus

    model_config = {"from_attributes": True}


class MaterialStatusResponse(BaseModel):
    id: uuid.UUID
    status: MaterialStatus
