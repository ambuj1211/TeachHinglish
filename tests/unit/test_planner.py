from teachhinglish.core.models import TeachingRequest
from teachhinglish.graph.planner import plan_teaching
from teachhinglish.graph.state import TeachingState


def test_plan_teaching_creates_structured_plan():
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    state = TeachingState(request=request)

    result = plan_teaching(state)

    assert result is state

    assert result.plan.learning_objectives
    assert result.plan.prerequisites
    assert result.plan.concepts
    assert result.plan.examples
    assert result.plan.teaching_sequence

    assert any(
        "Newton's Second Law" in objective
        for objective in result.plan.learning_objectives
    )

    assert "Newton's Second Law" in result.plan.concepts

    assert result.plan.teaching_sequence == [
        "Introduce the topic.",
        "Explain the prerequisites.",
        "Build the core concepts from basic to advanced.",
        "Demonstrate the concepts with examples.",
        "Summarize the important points.",
    ]