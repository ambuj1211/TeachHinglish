from teachhinglish.core.models import TeachingRequest
from teachhinglish.graph.state import TeachingState
from teachhinglish.validation.base import ValidationResult
from teachhinglish.validation.mathematics import MathematicsValidator
from teachhinglish.validation.pipeline import ValidationPipeline
from teachhinglish.validation.topic_coverage import TopicCoverageValidator
from teachhinglish.validation.content import ContentValidator
from teachhinglish.validation.structure import StructureValidator
from teachhinglish.validation.topic_coverage import TopicCoverageValidator


def validate_teaching_script(state: TeachingState) -> TeachingState:
    """Run all configured validators against the generated teaching script."""

    pipeline = ValidationPipeline(
        [
            _BasicScriptValidator(),
            StructureValidator(),
            ContentValidator(),
            TopicCoverageValidator(),
            MathematicsValidator(),
        ]
    )

    result = pipeline.validate(
        state.request,
        state.teaching_script,
    )

    state.validation_errors = result.errors
    state.validation_passed = result.passed

    return state


class _BasicScriptValidator:
    """Perform deterministic basic validation of a teaching script."""

    def validate(
        self,
        request: TeachingRequest,
        script: str,
    ) -> ValidationResult:
        errors: list[str] = []

        if not script.strip():
            errors.append("Teaching script is empty.")

        if request.topic.lower() not in script.lower():
            errors.append(
                "Teaching script does not mention the requested topic."
            )

        return ValidationResult(errors=errors)