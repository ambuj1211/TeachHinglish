import pytest

from teachhinglish.core.engine import TeacherLanguageEngine
from teachhinglish.core.models import (
    EducationLevel,
    Subject,
    TeachingRequest,
)
from teachhinglish.prompts.base import PromptBuilder
from teachhinglish.providers.base import LLMProvider


class FakeProvider(LLMProvider):
    async def generate(self, prompt: str, subject: Subject) -> str:
        assert subject == Subject.PHYSICS
        assert "Newton's Second Law" in prompt

        return "Hello bachcho, aaj hum Newton's Second Law samjhenge."


class FakePromptBuilder(PromptBuilder):
    def build(self, request: TeachingRequest, subject_context: str) -> str:
        return (
            f"Teach {request.topic} "
            f"for {request.education_level.value}. "
            f"{subject_context}"
        )


@pytest.mark.asyncio
async def test_teaching_engine():
    engine = TeacherLanguageEngine(
        provider=FakeProvider(),
        prompt_builder=FakePromptBuilder(),
    )

    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    response = await engine.teach(request)

    assert response.topic == "Newton's Second Law"
    assert response.subject == Subject.PHYSICS
    assert response.education_level == EducationLevel.CLASS_11
    assert response.exam_goal == "jee"
    assert response.language.value == "hinglish"
    assert "Newton's Second Law" in response.teaching_script