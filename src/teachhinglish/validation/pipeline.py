from teachhinglish.core.models import TeachingRequest
from teachhinglish.validation.base import ScriptValidator, ValidationResult


class ValidationPipeline:
    """Run multiple script validators and combine their results."""

    def __init__(self, validators: list[ScriptValidator]) -> None:
        self.validators = validators

    def validate(
        self,
        request: TeachingRequest,
        script: str,
    ) -> ValidationResult:
        errors: list[str] = []

        for validator in self.validators:
            result = validator.validate(request, script)
            errors.extend(result.errors)

        return ValidationResult(errors=errors)