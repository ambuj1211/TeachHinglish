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
    assert "Newton's Second Law" in result.plan.learning_objectives[0]

    assert result.plan.concepts == ["Newton's Second Law"]

    assert result.plan.teaching_sequence == [
        "Introduce the topic.",
        "Explain the core concept.",
        "Work through examples.",
        "Summarize the key points.",
    ]

    # Planner should no longer own the final LLM prompt.
    assert result.teaching_prompt == ""