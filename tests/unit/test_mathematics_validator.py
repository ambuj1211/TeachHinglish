from teachhinglish.core.models import TeachingRequest
from teachhinglish.validation.mathematics import (
    MathematicsValidator,
    validate_mathematical_expressions,
)


def make_request() -> TeachingRequest:
    return TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )


def test_valid_mathematical_expression():
    errors = validate_mathematical_expressions(
        """
        Newton's Second Law:
        F = m*a
        """
    )

    assert errors == []


def test_valid_numeric_expression():
    errors = validate_mathematical_expressions(
        """
        m = 2
        F = 10
        a = F/m
        """
    )

    assert errors == []


def test_invalid_mathematical_expression():
    errors = validate_mathematical_expressions(
        """
        a = F/
        """
    )

    assert len(errors) == 1
    assert "mathematical expression is invalid" in errors[0]


def test_normal_teaching_text_is_ignored():
    errors = validate_mathematical_expressions(
        """
        Today we will learn Newton's Second Law.
        Force and acceleration are related.
        """
    )

    assert errors == []


def test_valid_numeric_calculation_passes():
    script = """
    Force is given by:
    F = 2 * 5
    """

    errors = validate_mathematical_expressions(script)

    assert errors == []


def test_invalid_numeric_calculation_is_detected():
    script = """
    Force is given by:
    F = 2 + 5
    """

    errors = validate_mathematical_expressions(script)

    assert errors == []


def test_valid_algebraic_expression_passes():
    script = """
    Newton's Second Law:
    F = m * a
    """

    errors = validate_mathematical_expressions(script)

    assert errors == []


def test_incomplete_expression_fails():
    script = """
    Newton's Second Law:
    a = F /
    """

    errors = validate_mathematical_expressions(script)

    assert errors
    assert "mathematical expression is invalid" in errors[0]


def test_inline_latex_equation_passes():
    script = r"""
    Newton's Second Law is:
    \( F = ma \)
    """

    errors = validate_mathematical_expressions(script)

    assert errors == []


def test_latex_block_equation_passes():
    script = r"""
    Newton's Second Law:
    $$ F = ma $$
    """

    errors = validate_mathematical_expressions(script)

    assert errors == []


def test_latex_fraction_equation_passes():
    script = r"""
    Momentum is:
    $$ \vec{p} = m\vec{v} $$
    """

    errors = validate_mathematical_expressions(script)

    assert errors == []


def test_latex_power_expression_passes():
    script = r"""
    Kinetic energy is:
    $$ KE = \frac{1}{2}mv^2 $$
    """

    errors = validate_mathematical_expressions(script)

    assert errors == []


def test_malformed_latex_fraction_fails():
    script = r"""
    The formula is:
    $$ F = \frac{m}{ $$
    """

    errors = validate_mathematical_expressions(script)

    assert errors


def test_mathematics_validator_implements_validation_interface():
    validator = MathematicsValidator()

    result = validator.validate(
        make_request(),
        "F = m * a",
    )

    assert result.passed is True
    assert result.errors == []


def test_mathematics_validator_returns_errors():
    validator = MathematicsValidator()

    result = validator.validate(
        make_request(),
        "a = F /",
    )

    assert result.passed is False
    assert result.errors