from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import attempts, auth, contests, courses, dashboard, exam_plan, materials, quiz, weak_spots
from app.config import get_settings
from app.core.logging import configure_logging

configure_logging()

settings = get_settings()

app = FastAPI(title="Recall API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(courses.router, prefix="/courses", tags=["courses"])
app.include_router(materials.router, prefix="/materials", tags=["materials"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
app.include_router(attempts.router, prefix="/quiz/attempts", tags=["attempts"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(contests.router, prefix="/quiz/attempts", tags=["contests"])
app.include_router(exam_plan.router, prefix="/courses", tags=["exam-plan"])
app.include_router(weak_spots.router, prefix="/courses", tags=["weak-spots"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
