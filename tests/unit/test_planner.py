from teachhinglish.core.models import TeachingRequest
from teachhinglish.graph.planner import plan_teaching
from teachhinglish.graph.state import TeachingState


def test_plan_teaching_creates_prompt():
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    state = TeachingState(request=request)

    result = plan_teaching(state)

    assert result is state
    assert "Newton's Second Law" in result.teaching_prompt
    assert "class_11" in result.teaching_prompt
    assert "jee" in result.teaching_prompt