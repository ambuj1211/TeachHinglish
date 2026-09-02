from teachhinglish.core.models import TeachingRequest
from teachhinglish.validation.structure import StructureValidator


def make_request() -> TeachingRequest:
    return TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )


def test_valid_teaching_script_passes():
    script = """
    Today we will learn Newton's Second Law.

    Newton's Second Law explains the relationship between force,
    mass, and acceleration.

    For example, if a force acts on a body, its acceleration
    depends on the applied force and its mass.

    So the main idea is that force determines acceleration.
    """

    result = StructureValidator().validate(
        make_request(),
        script,
    )

    assert result.passed is True
    assert result.errors == []


def test_empty_script_fails():
    result = StructureValidator().validate(
        make_request(),
        "",
    )

    assert result.passed is False
    assert result.errors


def test_whitespace_only_script_fails():
    result = StructureValidator().validate(
        make_request(),
        "   \n\t  ",
    )

    assert result.passed is False
    assert result.errors


def test_extremely_short_script_fails():
    result = StructureValidator().validate(
        make_request(),
        "Newton's Second Law.",
    )

    assert result.passed is False
    assert any(
        "too short" in error.lower()
        for error in result.errors
    )


def test_json_like_output_fails():
    script = """
    {
        "topic": "Newton's Second Law",
        "answer": "Force is equal to mass times acceleration."
    }
    """

    result = StructureValidator().validate(
        make_request(),
        script,
    )

    assert result.passed is False
    assert result.errors


def test_model_metadata_labels_fail():
    script = """
    AI response:
    Generated response:
    Newton's Second Law explains force and acceleration.
    """

    result = StructureValidator().validate(
        make_request(),
        script,
    )

    assert result.passed is False
    assert result.errors