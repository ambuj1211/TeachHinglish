from dataclasses import dataclass, field

from teachhinglish.core.models import TeachingRequest


@dataclass
class TeachingState:
    """State carried through the TeachHinglish teaching graph."""

    request: TeachingRequest

    subject_context: str = ""
    teaching_prompt: str = ""
    teaching_script: str = ""

    validation_passed: bool = False
    validation_errors: list[str] = field(default_factory=list)

    retry_count: int = 0