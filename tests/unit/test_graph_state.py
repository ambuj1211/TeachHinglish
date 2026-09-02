from teachhinglish.core.models import TeachingRequest
from teachhinglish.graph.state import TeachingState


def test_teaching_state_defaults():
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    state = TeachingState(request=request)

    assert state.request == request
    assert state.subject_context == ""
    assert state.teaching_prompt == ""
    assert state.teaching_script == ""
    assert state.validation_passed is False
    assert state.validation_errors == []
    assert state.retry_count == 0


def test_teaching_state_can_store_pipeline_data():
    request = TeachingRequest(
        topic="Binary Search Tree",
        subject="computer_science",
        education_level="btech",
        exam_goal="semester",
    )

    state = TeachingState(
        request=request,
        subject_context="BST subject context",
        teaching_prompt="Teach BST...",
        teaching_script="Hello friends...",
        validation_passed=True,
        validation_errors=[],
        retry_count=1,
    )

    assert state.subject_context == "BST subject context"
    assert state.teaching_prompt == "Teach BST..."
    assert state.teaching_script == "Hello friends..."
    assert state.validation_passed is True
    assert state.retry_count == 1