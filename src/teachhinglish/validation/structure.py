from teachhinglish.validation.base import ValidationResult
from teachhinglish.core.models import TeachingRequest
from teachhinglish.validation.base import ValidationResult


class StructureValidator:
    """Validate the basic structure and output format of a teaching script."""

    _MIN_WORD_COUNT = 20

    def validate(
        self,
        request: TeachingRequest,
        script: str,
    ) -> ValidationResult:
        errors: list[str] = []

        stripped = script.strip()

        if not stripped:
            errors.append("Teaching script is empty.")
            return ValidationResult(errors=errors)

        word_count = len(stripped.split())

        if word_count < self._MIN_WORD_COUNT:
            errors.append("Teaching script is too short.")

        if self._looks_like_json(stripped):
            errors.append("Teaching script contains JSON output.")

        if self._contains_metadata_label(stripped):
            errors.append("Teaching script contains model metadata.")

        return ValidationResult(errors=errors)

    @staticmethod
    def _looks_like_json(script: str) -> bool:
        stripped = script.strip()

        return (
            (stripped.startswith("{") and stripped.endswith("}"))
            or (stripped.startswith("[") and stripped.endswith("]"))
        )

    @staticmethod
    def _contains_metadata_label(script: str) -> bool:
        lowered = script.lower()

        metadata_labels = (
            "ai response:",
            "generated response:",
        )

        return any(label in lowered for label in metadata_labels)