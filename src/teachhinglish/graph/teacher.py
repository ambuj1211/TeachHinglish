from teachhinglish.core.settings import get_settings
from teachhinglish.graph.state import TeachingState
from teachhinglish.providers.gemini import GeminiProvider
from teachhinglish.providers.gemini_key_resolver import GeminiKeyResolver


async def generate_teaching_script(state: TeachingState) -> TeachingState:
    """Generate the teaching script using the configured Gemini provider."""

    settings = get_settings()
    resolver = GeminiKeyResolver(settings)
    provider = GeminiProvider(settings, resolver)

    prompt = state.teaching_prompt

    if state.validation_errors:
        validation_feedback = "\n".join(
            f"- {error}" for error in state.validation_errors
        )

        prompt = (
            f"{prompt}\n\n"
            "VALIDATION FEEDBACK\n"
            "The previous teaching script failed validation.\n\n"
            "PREVIOUS TEACHING SCRIPT\n"
            f"{state.teaching_script}\n\n"
            "ERRORS\n"
            f"{validation_feedback}\n\n"
            "Do not repeat the validation errors.\n"
            "Return only the corrected teaching script."
        )

    response = await provider.generate(
        prompt,
        state.request.subject.value,
    )

    state.teaching_script = response

    return state