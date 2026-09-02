from teachhinglish.core.models import TeachingRequest
from teachhinglish.graph.prompt import build_teaching_prompt
from teachhinglish.graph.state import TeachingState


def test_build_teaching_prompt():
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    state = TeachingState(
        request=request,
        subject_context="Physics knowledge context",
    )

    result = build_teaching_prompt(state)

    assert result is state
    assert result.teaching_prompt
    assert "Newton's Second Law" in result.teaching_prompt
    assert "Physics knowledge context" in result.teaching_prompt
    assert "class_11" in result.teaching_prompt