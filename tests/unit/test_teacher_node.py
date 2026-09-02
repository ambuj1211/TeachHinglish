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

class RetryAwareFakeProvider:
    async def generate(self, prompt: str, subject: str) -> str:
        assert "Newton's Second Law" in prompt
        assert "VALIDATION FEEDBACK" in prompt
        assert "mathematical expression is invalid" in prompt
        assert "a = F /" in prompt
        assert subject == "physics"

        return "Corrected teaching script."


@pytest.mark.asyncio
async def test_generate_teaching_script_includes_validation_feedback_on_retry(
    monkeypatch,
):
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    state = TeachingState(
        request=request,
        teaching_prompt="Teach Newton's Second Law for Class 11 JEE.",
        teaching_script="Newton's Second Law:\na = F /",
        validation_errors=[
            "mathematical expression is invalid: cannot parse 'F /'"
        ],
        retry_count=1,
    )

    fake_provider = RetryAwareFakeProvider()

    monkeypatch.setattr(
        "teachhinglish.graph.teacher.GeminiProvider",
        lambda settings, resolver: fake_provider,
    )

    result = await generate_teaching_script(state)

    assert result is state
    assert result.teaching_script == "Corrected teaching script."

class InitialGenerationFakeProvider:
    async def generate(self, prompt: str, subject: str) -> str:
        assert "VALIDATION FEEDBACK" not in prompt
        return "Initial teaching script."


@pytest.mark.asyncio
async def test_generate_teaching_script_does_not_include_validation_feedback_on_first_attempt(
    monkeypatch,
):
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    state = TeachingState(
        request=request,
        teaching_prompt="Teach Newton's Second Law for Class 11 JEE.",
        retry_count=0,
    )

    fake_provider = InitialGenerationFakeProvider()

    monkeypatch.setattr(
        "teachhinglish.graph.teacher.GeminiProvider",
        lambda settings, resolver: fake_provider,
    )

    result = await generate_teaching_script(state)

    assert result is state
    assert result.teaching_script == "Initial teaching script."