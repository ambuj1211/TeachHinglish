from teachhinglish.core.models import TeachingRequest
from teachhinglish.graph.state import TeachingState
from teachhinglish.graph.workflow import (
    MAX_VALIDATION_RETRIES,
    _validation_route,
     build_teaching_graph,
)

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

def test_validation_route_ends_when_validation_passes():
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    state = TeachingState(
        request=request,
        validation_passed=True,
    )

    result = _validation_route(state)

    assert result == "end"
    assert state.retry_count == 0


def test_validation_route_retries_when_validation_fails():
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    state = TeachingState(
        request=request,
        validation_passed=False,
        retry_count=0,
    )

    result = _validation_route(state)

    assert result == "retry"
    assert state.retry_count == 1


def test_validation_route_stops_after_max_retries():
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    state = TeachingState(
        request=request,
        validation_passed=False,
        retry_count=MAX_VALIDATION_RETRIES,
    )

    result = _validation_route(state)

    assert result == "end"
    assert state.retry_count == MAX_VALIDATION_RETRIES