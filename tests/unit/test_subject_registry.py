import pytest

from teachhinglish.core.models import Subject
from teachhinglish.subjects.registry import (
    SUBJECT_PROFILES,
    get_subject_profile,
)


def test_all_subjects_have_profiles():
    assert set(SUBJECT_PROFILES) == set(Subject)


@pytest.mark.parametrize(
    ("subject", "expected_name"),
    [
        (Subject.PHYSICS, "Physics"),
        (Subject.MATHEMATICS, "Mathematics"),
        (Subject.COMPUTER_SCIENCE, "Computer Science"),
        (Subject.DIGITAL_LOGIC, "Digital Logic"),
    ],
)
def test_subject_profile(subject, expected_name):
    profile = get_subject_profile(subject)

    assert profile.subject == subject
    assert profile.display_name == expected_name
    assert profile.description
