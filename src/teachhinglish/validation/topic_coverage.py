from teachhinglish.core.models import TeachingRequest
from teachhinglish.validation.base import ValidationResult


class TopicCoverageValidator:
    """Validate that a teaching script meaningfully covers its topic."""

    MIN_SCRIPT_WORDS = 25

    def validate(
        self,
        request: TeachingRequest,
        script: str,
    ) -> ValidationResult:
        errors: list[str] = []

        normalized_script = script.strip()

        if not normalized_script:
            return ValidationResult(
                errors=["Topic coverage validation failed: script is empty."]
            )

        words = normalized_script.split()

        if len(words) < self.MIN_SCRIPT_WORDS:
            errors.append(
                "Topic coverage validation failed: "
                "teaching script is too short to explain the topic."
            )

        topic = request.topic.strip().lower()

        if topic and topic not in normalized_script.lower():
            errors.append(
                "Topic coverage validation failed: "
                "requested topic is not mentioned in the script."
            )

        return ValidationResult(errors=errors)