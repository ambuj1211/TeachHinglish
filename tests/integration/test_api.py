import pytest
from fastapi.testclient import TestClient

from teachhinglish.api.app import app
from teachhinglish.core.models import TeachingResponse


class FakeEngine:
    async def teach(self, request):
        return TeachingResponse(
            topic=request.topic,
            subject=request.subject,
            education_level=request.education_level,
            exam_goal=request.exam_goal,
            language=request.language,
            style=request.style,
            teaching_script=(
                "Hello bachcho, aaj hum Newton's Second Law samjhenge."
            ),
        )


def test_health():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_engine():
    from teachhinglish.api.app import create_engine

    engine = create_engine()

    assert engine is not None


def test_teach_endpoint(monkeypatch):
    from teachhinglish.api import app as api_module

    monkeypatch.setattr(
        api_module,
        "create_engine",
        lambda: FakeEngine(),
    )

    client = TestClient(app)

    response = client.post(
        "/v1/teach",
        json={
            "topic": "Newton's Second Law",
            "subject": "physics",
            "education_level": "jee",
            "exam_goal": "conceptual understanding",
            "language": "hinglish",
            "style": "conceptual",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["topic"] == "Newton's Second Law"
    assert data["subject"] == "physics"
    assert data["education_level"] == "jee"
    assert data["exam_goal"] == "conceptual understanding"
    assert data["language"] == "hinglish"
    assert data["style"] == "conceptual"
    assert (
        data["teaching_script"]
        == "Hello bachcho, aaj hum Newton's Second Law samjhenge."
    )