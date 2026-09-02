from fastapi import FastAPI

from teachhinglish.core.engine import TeacherLanguageEngine
from teachhinglish.core.models import TeachingRequest, TeachingResponse
from teachhinglish.core.settings import get_settings
from teachhinglish.prompts.teaching import TeachingPromptBuilder
from teachhinglish.providers.gemini import GeminiProvider
from teachhinglish.providers.gemini_key_resolver import GeminiKeyResolver


def create_engine() -> TeacherLanguageEngine:
    settings = get_settings()

    key_resolver = GeminiKeyResolver(settings)
    provider = GeminiProvider(settings, key_resolver)
    prompt_builder = TeachingPromptBuilder()

    return TeacherLanguageEngine(
        provider=provider,
        prompt_builder=prompt_builder,
    )


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