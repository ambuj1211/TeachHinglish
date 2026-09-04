from teachhinglish.graph.state import TeachingState
from teachhinglish.prompts.teaching import TeachingPromptBuilder


def build_teaching_prompt(state: TeachingState) -> TeachingState:
    """Build the final LLM prompt from the current teaching state."""

    builder = TeachingPromptBuilder()

    state.teaching_prompt = builder.build(
        state.request,
        state.subject_context,
        state.plan,
    )

    return state