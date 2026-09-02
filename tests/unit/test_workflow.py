from teachhinglish.core.models import TeachingRequest
from teachhinglish.graph.state import TeachingState
from teachhinglish.graph.workflow import build_teaching_graph


def test_teaching_graph_is_compilable():
    graph = build_teaching_graph()

    assert graph is not None


def test_teaching_state_defaults():
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    state = TeachingState(request=request)

    assert state.subject_context == ""
    assert state.teaching_prompt == ""
    assert state.teaching_script == ""
    assert state.validation_passed is False
    assert state.validation_errors == []
    assert state.retry_count == 0