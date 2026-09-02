from teachhinglish.core.models import TeachingRequest
from teachhinglish.graph.state import TeachingState
from teachhinglish.graph.validator import validate_teaching_script


def make_state(script: str) -> TeachingState:
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    return TeachingState(
        request=request,
        teaching_script=script,
    )


def test_valid_teaching_script():
    state = make_state(
        """
        Today we will understand Newton's Second Law with simple examples.

        Newton's Second Law explains how the net force acting on an object
        determines its acceleration.

        The relationship is represented by:
        F = m * a

        Here, force, mass, and acceleration are connected by this equation.

        For example, if a 2 kg object experiences a net force of 10 N,
        its acceleration is 5 m/s^2.

        In conclusion, Newton's Second Law tells us that net force equals
        mass multiplied by acceleration.
        """
    )

    result = validate_teaching_script(state)

    assert result is state
    assert result.validation_passed is True
    assert result.validation_errors == []


def test_empty_teaching_script_fails():
    state = make_state("")

    result = validate_teaching_script(state)

    assert result.validation_passed is False
    assert "Teaching script is empty." in result.validation_errors


def test_missing_topic_fails():
    state = make_state(
        "Today we will learn about force and acceleration."
    )

    result = validate_teaching_script(state)

    assert result.validation_passed is False
    assert "Teaching script does not mention the requested topic." in (
        result.validation_errors
    )


def test_invalid_mathematics_fails_validation():
    state = make_state(
        """
        Newton's Second Law:
        F = ma
        a = F/
        """
    )

    result = validate_teaching_script(state)

    assert result.validation_passed is False
    assert any(
        "mathematical expression is invalid" in error.lower()
        for error in result.validation_errors
    )


def test_valid_mathematics_passes_validation():
    state = make_state(
        """
        Newton's Second Law explains the relationship between force,
        mass, and acceleration.

        The equation is F = m * a, where F represents net force,
        m represents mass, and a represents acceleration.

        For example, if the mass is 2 kg and the net force is 10 N,
        the acceleration is 5 m/s^2.

        This means that increasing the net force increases acceleration
        when the mass remains constant.

        In conclusion, Newton's Second Law relates net force, mass,
        and acceleration through the equation F = m * a.
        """
    )

    result = validate_teaching_script(state)

    assert result.validation_passed is True
    assert result.validation_errors == []