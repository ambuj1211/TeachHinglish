from teachhinglish.core.models import TeachingRequest
from teachhinglish.validation.base import ValidationResult
from teachhinglish.validation.pipeline import ValidationPipeline
from teachhinglish.validation.structure import StructureValidator
from teachhinglish.validation.content import ContentValidator


def make_request() -> TeachingRequest:
    return TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )


class PassingValidator:
    def validate(
        self,
        request: TeachingRequest,
        script: str,
    ) -> ValidationResult:
        return ValidationResult(errors=[])


class FailingValidator:
    def validate(
        self,
        request: TeachingRequest,
        script: str,
    ) -> ValidationResult:
        return ValidationResult(
            errors=["Test validation error."]
        )


def test_pipeline_passes_when_all_validators_pass():
    pipeline = ValidationPipeline(
        [
            PassingValidator(),
            PassingValidator(),
        ]
    )

    result = pipeline.validate(
        make_request(),
        "some teaching script",
    )

    assert result.passed is True
    assert result.errors == []


def test_pipeline_combines_errors_from_all_validators():
    pipeline = ValidationPipeline(
        [
            FailingValidator(),
            FailingValidator(),
        ]
    )

    result = pipeline.validate(
        make_request(),
        "some teaching script",
    )

    assert result.passed is False
    assert result.errors == [
        "Test validation error.",
        "Test validation error.",
    ]


def test_pipeline_runs_structure_validator():
    pipeline = ValidationPipeline(
        [
            StructureValidator(),
        ]
    )

    result = pipeline.validate(
        make_request(),
        "Newton's Second Law.",
    )

    assert result.passed is False
    assert any(
        "too short" in error.lower()
        for error in result.errors
    )


def test_pipeline_combines_structure_and_custom_validator():
    pipeline = ValidationPipeline(
        [
            StructureValidator(),
            FailingValidator(),
        ]
    )

    result = pipeline.validate(
        make_request(),
        """
        Today we will learn Newton's Second Law.

        Newton's Second Law explains the relationship between force,
        mass, and acceleration.

        For example, if a force acts on a body, its acceleration
        depends on the applied force and its mass.

        So the main idea is that force determines acceleration.
        """,
    )

    assert result.passed is False
    assert "Test validation error." in result.errors


def test_pipeline_runs_content_validator():
    pipeline = ValidationPipeline(
        [
            ContentValidator(),
        ]
    )

    result = pipeline.validate(
        make_request(),
        "Newton's Second Law",
    )

    assert result.passed is False
    assert result.errors


def test_pipeline_content_validator_accepts_good_script():
    pipeline = ValidationPipeline(
        [
            ContentValidator(),
        ]
    )

    result = pipeline.validate(
        make_request(),
        """
        Today we will learn Newton's Second Law.

        Newton's Second Law explains the relationship between
        force, mass, and acceleration.

        For example, if a force acts on a body, its acceleration
        depends on the applied force and its mass.

        In conclusion, remember that Newton's Second Law relates
        net force, mass, and acceleration.
        """,
    )

    assert result.passed is True
    assert result.errors == []