import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models.course import Course
from app.db.models.material import Material, MaterialStatus, SourceType
from app.db.models.user import User
from app.db.session import SessionLocal, get_db
from app.schemas.material import MaterialResponse, MaterialStatusResponse
from app.services.ingest import ingest_material

router = APIRouter()

_EXT_TO_SOURCE_TYPE = {"pdf": SourceType.pdf, "md": SourceType.md, "txt": SourceType.txt}


async def _run_ingest_in_background(material_id: uuid.UUID, raw_bytes: bytes) -> None:
    db = SessionLocal()
    try:
        await ingest_material(db, material_id, raw_bytes)
    finally:
        db.close()


@router.post("/upload", response_model=MaterialResponse, status_code=status.HTTP_201_CREATED)
async def upload_material(
    background_tasks: BackgroundTasks,
    file: UploadFile,
    course_id: uuid.UUID,
    module_id: uuid.UUID | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Material:
    course = db.get(Course, course_id)
    if course is None or course.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Course not found")

    ext = (file.filename or "").rsplit(".", 1)[-1].lower()
    source_type = _EXT_TO_SOURCE_TYPE.get(ext)
    if source_type is None:
        raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF, MD, or TXT.")

    material = Material(
        course_id=course_id,
        module_id=module_id,
        filename=file.filename or "untitled",
        source_type=source_type,
        status=MaterialStatus.processing,
    )
    db.add(material)
    db.commit()
    db.refresh(material)

    raw_bytes = await file.read()
    background_tasks.add_task(_run_ingest_in_background, material.id, raw_bytes)

    return material


@router.get("", response_model=list[MaterialResponse])
def list_materials(
    course_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[Material]:
    course = db.get(Course, course_id)
    if course is None or course.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Course not found")

    stmt = select(Material).where(Material.course_id == course_id).order_by(Material.created_at.desc())
    return list(db.execute(stmt).scalars().all())


@router.get("/{material_id}/status", response_model=MaterialStatusResponse)
def get_material_status(
    material_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> Material:
    material = db.get(Material, material_id)
    if material is None or material.course.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Material not found")
    return material
