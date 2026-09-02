from abc import ABC, abstractmethod

from teachhinglish.core.models import Subject


class LLMProvider(ABC):
    """Interface implemented by LLM backends."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        subject: Subject,
    ) -> str:
        """Generate text using the provider."""
        raise NotImplementedError