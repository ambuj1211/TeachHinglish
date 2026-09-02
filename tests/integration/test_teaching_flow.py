import pytest

from teachhinglish.core.engine import TeacherLanguageEngine
from teachhinglish.core.models import Subject, TeachingRequest
from teachhinglish.graph import teacher as teacher_module


class FakeProvider:
    async def generate(self, prompt: str, subject: Subject) -> str:
        assert subject == Subject.PHYSICS
        assert "Newton's Second Law" in prompt

        return """
        Hello bachcho, aaj hum Newton's Second Law samjhenge.

        Newton's Second Law explains the relationship between
        force, mass, and acceleration.

        The equation is:

        F = m * a

        For example, if a force of 10 N acts on a mass of 2 kg,
        acceleration is 5 m/s^2.

        So, Newton's Second Law tells us how force affects acceleration.
        In summary, F = m * a is the key relationship to remember.
        """


@pytest.mark.asyncio
async def test_complete_teaching_flow(monkeypatch):
    fake_provider = FakeProvider()

    monkeypatch.setattr(
        teacher_module,
        "GeminiProvider",
        lambda settings, resolver: fake_provider,
    )

    engine = TeacherLanguageEngine()

    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    response = await engine.teach(request)

    assert response.topic == "Newton's Second Law"
    assert response.subject == Subject.PHYSICS
    assert response.teaching_script

    assert "Newton's Second Law" in response.teaching_script
    assert "F = m * a" in response.teaching_script