import app.db.base  # noqa: F401
from app.db.session import SessionLocal
from app.db.models.material import Material
from app.db.models.subject import Subject
from app.db.models.chunk import Chunk

db = SessionLocal()
try:
    for s in db.query(Subject).all():
        print(f"SUBJECT: {s.name} ({s.id})")
        for m in db.query(Material).filter(Material.subject_id == s.id).all():
            chunk_count = db.query(Chunk).filter(Chunk.material_id == m.id).count()
            print(f"  - {m.filename} | status={m.status} | chunks={chunk_count}")
finally:
    db.close()
