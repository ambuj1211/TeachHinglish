import re

from teachhinglish.validation.base import ScriptValidator, ValidationResult
from teachhinglish.core.models import TeachingRequest
from teachhinglish.validation.base import ValidationResult


class ContentValidator(ScriptValidator):
    """Validate basic teaching-content quality."""

    MIN_WORD_COUNT = 30

    PLACEHOLDER_PATTERNS = (
        r"\[TODO\]",
        r"\[INSERT[^\]]*\]",
        r"\[ADD[^\]]*\]",
        r"\bTODO\b",
    )

    META_PATTERNS = (
        r"\bas an ai\b",
        r"\bi cannot\b",
        r"\bi'm unable\b",
        r"\bas a language model\b",
    )

    def validate(
        self,
        request: TeachingRequest,
        script: str,
    ) -> ValidationResult:
        errors: list[str] = []

        normalized = script.strip()

        if not normalized:
            errors.append("Teaching content is empty.")
            return ValidationResult(errors=errors)

        word_count = len(normalized.split())

        if word_count < self.MIN_WORD_COUNT:
            errors.append(
                f"Teaching content is too short "
                f"(minimum {self.MIN_WORD_COUNT} words)."
            )

        for pattern in self.PLACEHOLDER_PATTERNS:
            if re.search(pattern, normalized, re.IGNORECASE):
                errors.append(
                    "Teaching content contains unfinished placeholder text."
                )
                break

        for pattern in self.META_PATTERNS:
            if re.search(pattern, normalized, re.IGNORECASE):
                errors.append(
                    "Teaching content contains AI/meta-generation text."
                )
                break

        if not re.search(
            r"\b(for example|example|e\.g\.|suppose|consider)\b",
            normalized,
            re.IGNORECASE,
        ):
            errors.append(
                "Teaching content does not contain an example."
            )

        if not re.search(
            r"\b(in conclusion|to summarize|summary|remember|key point)\b",
            normalized,
            re.IGNORECASE,
        ):
            errors.append(
                "Teaching content does not contain a conclusion or summary."
            )

        return ValidationResult(errors=errors)