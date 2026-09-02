from teachhinglish.core.settings import get_settings
from teachhinglish.graph.state import TeachingState
from teachhinglish.providers.gemini import GeminiProvider
from teachhinglish.providers.gemini_key_resolver import GeminiKeyResolver


async def generate_teaching_script(state: TeachingState) -> TeachingState:
    """Generate the teaching script using the configured Gemini provider."""

    settings = get_settings()
    resolver = GeminiKeyResolver(settings)
    provider = GeminiProvider(settings, resolver)

    response = await provider.generate(
        state.teaching_prompt,
        state.request.subject.value,
    )

    state.teaching_script = response

    return state