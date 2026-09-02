from teachhinglish.validation.base import ValidationResult


def test_validation_result_passes_without_errors():
    result = ValidationResult(errors=[])

    assert result.passed is True


def test_validation_result_fails_with_errors():
    result = ValidationResult(
        errors=["Mathematical expression is invalid."]
    )

    assert result.passed is False
    assert result.errors == ["Mathematical expression is invalid."]