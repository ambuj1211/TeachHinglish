import time

from google import genai

from teachhinglish.core.models import Subject
from teachhinglish.core.settings import Settings
from teachhinglish.providers.gemini_key_resolver import GeminiKeyResolver


class GeminiProvider:
    """Gemini LLM provider with subject-based API-key routing."""

    def __init__(
        self,
        settings: Settings,
        key_resolver: GeminiKeyResolver,
    ) -> None:
        self.settings = settings
        self.key_resolver = key_resolver

    async def generate(
        self,
        prompt: str,
        subject: Subject,
    ) -> str:
        """Generate a response using the Gemini key for the subject."""

        api_key = self.key_resolver.resolve(subject.value)

        if not api_key:
            raise RuntimeError(
                f"No Gemini API key configured for subject: {subject.value}"
            )

        client = genai.Client(api_key=api_key)

        start = time.perf_counter()

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        elapsed = time.perf_counter() - start

        text = response.text or ""

        if not text.strip():
            raise RuntimeError("Gemini returned an empty response")

        return text.strip()
