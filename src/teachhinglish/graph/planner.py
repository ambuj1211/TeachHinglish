from teachhinglish.graph.state import TeachingState


def plan_teaching(state: TeachingState) -> TeachingState:
    """Prepare the teaching plan from the request."""

    state.teaching_prompt = (
        f"Teach {state.request.topic} for "
        f"{state.request.education_level.value} level "
        f"with {state.request.exam_goal or 'general learning'} "
        f"as the goal."
    )

    return state