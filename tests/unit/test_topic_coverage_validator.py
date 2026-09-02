from teachhinglish.core.models import TeachingRequest
from teachhinglish.validation.base import ValidationResult
from teachhinglish.validation.topic_coverage import TopicCoverageValidator


def make_request(topic: str = "Newton's Second Law") -> TeachingRequest:
    return TeachingRequest(
        topic=topic,
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )


def test_meaningful_topic_explanation_passes():
    validator = TopicCoverageValidator()

    script = """
    Newton's Second Law explains how the net force acting on an object
    determines its acceleration.

    The relationship is F = m * a.

    Here, F represents force, m represents mass, and a represents
    acceleration. For a fixed mass, increasing the net force increases
    the acceleration.
    """

    result = validator.validate(make_request(), script)

    assert result.passed is True
    assert result.errors == []


def test_topic_only_mention_fails():
    validator = TopicCoverageValidator()

    script = """
    Today we will learn Newton's Second Law.

    Physics is an important subject.
    Force is measured in newtons.
    """

    result = validator.validate(make_request(), script)

    assert result.passed is False
    assert result.errors


def test_empty_script_fails():
    validator = TopicCoverageValidator()

    result = validator.validate(make_request(), "")

    assert result.passed is False
    assert result.errors


def test_very_short_explanation_fails():
    validator = TopicCoverageValidator()

    script = """
    Newton's Second Law is about force and acceleration.
    """

    result = validator.validate(make_request(), script)

    assert result.passed is False
    assert result.errors


def test_case_difference_does_not_cause_failure():
    validator = TopicCoverageValidator()

    script = """
    NEWTON'S SECOND LAW explains the relationship between force,
    mass, and acceleration.

    The equation is F = m * a. A larger net force produces a larger
    acceleration when the mass remains constant.
    """

    result = validator.validate(make_request(), script)

    assert result.passed is True