from teachhinglish.graph.state import TeachingState


def load_knowledge(state: TeachingState) -> TeachingState:
    """Load subject knowledge context for the requested topic."""

    state.subject_context = (
        f"Subject: {state.request.subject.value}\n"
        f"Topic: {state.request.topic}\n"
        f"Education level: {state.request.education_level.value}\n"
        f"Exam goal: {state.request.exam_goal or 'general learning'}"
    )

    return state