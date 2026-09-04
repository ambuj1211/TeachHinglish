from teachhinglish.core.plan import TeachingPlan
from teachhinglish.graph.state import TeachingState


def plan_teaching(state: TeachingState) -> TeachingState:
    """Prepare a structured teaching plan from the request."""

    state.plan = TeachingPlan(
        learning_objectives=[
            f"Understand the concept of {state.request.topic}.",
        ],
        prerequisites=[],
        concepts=[
            state.request.topic,
        ],
        examples=[],
        teaching_sequence=[
            "Introduce the topic.",
            "Explain the core concept.",
            "Work through examples.",
            "Summarize the key points.",
        ],
    )

    return state