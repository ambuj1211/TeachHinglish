from dataclasses import dataclass
from typing import Protocol

from teachhinglish.core.models import TeachingRequest


@dataclass(frozen=True)
class ValidationResult:
    errors: list[str]

    @property
    def passed(self) -> bool:
        return not self.errors


class ScriptValidator(Protocol):
    def validate(
        self,
        request: TeachingRequest,
        script: str,
    ) -> ValidationResult:
        ...