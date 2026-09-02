from fastapi import FastAPI

from teachhinglish.core.engine import TeacherLanguageEngine
from teachhinglish.core.models import TeachingRequest, TeachingResponse


def create_engine() -> TeacherLanguageEngine:
    return TeacherLanguageEngine()


app = FastAPI(
    title="TeachHinglish API",
    description=(
        "AI teacher-language engine for natural, "
        "subject-aware educational Hinglish."
    ),
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/teach", response_model=TeachingResponse)
async def teach(request: TeachingRequest) -> TeachingResponse:
    engine = create_engine()
    return await engine.teach(request)