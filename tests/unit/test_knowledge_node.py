from teachhinglish.core.models import TeachingRequest
from teachhinglish.graph.knowledge import load_knowledge
from teachhinglish.graph.state import TeachingState


def test_load_knowledge_creates_subject_context():
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    state = TeachingState(request=request)

    result = load_knowledge(state)

    assert result is state
    assert "physics" in result.subject_context
    assert "Newton's Second Law" in result.subject_context
    assert "class_11" in result.subject_context
    assert "jee" in result.subject_context