import pytest

from teachhinglish.core.models import TeachingRequest
from teachhinglish.graph.state import TeachingState
from teachhinglish.graph.teacher import generate_teaching_script


class FakeProvider:
    async def generate(self, prompt: str, subject: str) -> str:
        assert "Newton's Second Law" in prompt
        assert subject == "physics"

        return "Newton's Second Law explains the relation between force and acceleration."


@pytest.mark.asyncio
async def test_generate_teaching_script(monkeypatch):
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    state = TeachingState(
        request=request,
        teaching_prompt="Teach Newton's Second Law for Class 11 JEE.",
    )

    fake_provider = FakeProvider()

    monkeypatch.setattr(
        "teachhinglish.graph.teacher.GeminiProvider",
        lambda settings, resolver: fake_provider,
    )

    result = await generate_teaching_script(state)

    assert result is state
    assert result.teaching_script
    assert "Newton's Second Law" in result.teaching_script