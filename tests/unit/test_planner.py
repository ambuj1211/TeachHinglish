import pytest

from teachhinglish.core.models import Subject, TeachingRequest
from teachhinglish.graph.planner import plan_teaching
from teachhinglish.graph.state import TeachingState


@pytest.mark.parametrize(
    ("subject", "topic", "expected_approach"),
    [
        (
            Subject.PHYSICS,
            "Newton's Second Law",
            "physical intuition",
        ),
        (
            Subject.MATHEMATICS,
            "Quadratic Equations",
            "mathematical reasoning",
        ),
        (
            Subject.CHEMISTRY,
            "Chemical Bonding",
            "reactions",
        ),
        (
            Subject.BIOLOGY,
            "Photosynthesis",
            "biological processes",
        ),
        (
            Subject.HISTORY,
            "Indian Independence Movement",
            "chronology",
        ),
        (
            Subject.CIVICS,
            "Fundamental Rights",
            "constitutional concepts",
        ),
        (
            Subject.GEOGRAPHY,
            "Monsoon",
            "spatial relationships",
        ),
        (
            Subject.ENGLISH_GRAMMAR,
            "Tenses",
            "grammar rules",
        ),
        (
            Subject.COMPUTER_SCIENCE,
            "Binary Search Tree",
            "algorithms",
        ),
        (
            Subject.ENGINEERING_MATHEMATICS,
            "Differential Equations",
            "mathematical theory",
        ),
        (
            Subject.DIGITAL_LOGIC,
            "Boolean Algebra",
            "Boolean algebra",
        ),
        (
            Subject.GENERAL,
            "Critical Thinking",
            "clear conceptual explanation",
        ),
    ],
)
def test_plan_teaching_is_subject_aware(
    subject,
    topic,
    expected_approach,
):
    request = TeachingRequest(
        topic=topic,
        subject=subject,
        education_level="general",
        exam_goal=None,
    )

    state = TeachingState(request=request)

    result = plan_teaching(state)

    assert result is state

    assert result.plan.learning_objectives
    assert result.plan.prerequisites
    assert result.plan.concepts
    assert result.plan.examples
    assert result.plan.teaching_sequence

    assert topic in result.plan.concepts

    assert any(
        expected_approach in concept
        for concept in result.plan.concepts
    )