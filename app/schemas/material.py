import uuid

from pydantic import BaseModel

from app.db.models.material import MaterialStatus, SourceType


class MaterialResponse(BaseModel):
    id: uuid.UUID
    subject_id: uuid.UUID
    filename: str
    source_type: SourceType
    status: MaterialStatus

    model_config = {"from_attributes": True}


class MaterialStatusResponse(BaseModel):
    id: uuid.UUID
    status: MaterialStatus
