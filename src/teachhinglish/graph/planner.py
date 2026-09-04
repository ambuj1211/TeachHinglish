from teachhinglish.core.plan import TeachingPlan
from teachhinglish.graph.state import TeachingState


def plan_teaching(state: TeachingState) -> TeachingState:
    """Create a structured teaching plan from the teaching request."""

    request = state.request

    state.plan = TeachingPlan(
        learning_objectives=[
            f"Understand the fundamentals of {request.topic}.",
            f"Explain the key concepts of {request.topic}.",
            f"Apply the concepts of {request.topic} at the expected {request.education_level.value} level.",
        ],
        prerequisites=[
            f"Basic knowledge required to understand {request.topic}.",
        ],
        concepts=[
            request.topic,
        ],
        examples=[
            f"Use a practical example to explain {request.topic}.",
        ],
        teaching_sequence=[
            "Introduce the topic.",
            "Explain the prerequisites.",
            "Build the core concepts from basic to advanced.",
            "Demonstrate the concepts with examples.",
            "Summarize the important points.",
        ],
    )

    return state