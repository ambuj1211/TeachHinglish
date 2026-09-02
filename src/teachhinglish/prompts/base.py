from abc import ABC, abstractmethod

from teachhinglish.core.models import TeachingRequest


class PromptBuilder(ABC):
    """Interface for constructing LLM teaching prompts."""

    @abstractmethod
    def build(self, request: TeachingRequest, subject_context: str) -> str:
        """Build the complete teaching prompt."""
        raise NotImplementedError
