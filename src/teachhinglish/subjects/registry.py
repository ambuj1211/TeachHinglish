from dataclasses import dataclass

from teachhinglish.core.models import Subject


@dataclass(frozen=True)
class SubjectProfile:
    subject: Subject
    display_name: str
    description: str


SUBJECT_PROFILES: dict[Subject, SubjectProfile] = {
    Subject.PHYSICS: SubjectProfile(
        Subject.PHYSICS,
        "Physics",
        "Physics concepts, numericals, derivations and problem solving.",
    ),
    Subject.MATHEMATICS: SubjectProfile(
        Subject.MATHEMATICS,
        "Mathematics",
        "Mathematical concepts, proofs, formulas and problem solving.",
    ),
    Subject.CHEMISTRY: SubjectProfile(
        Subject.CHEMISTRY,
        "Chemistry",
        "Physical, organic and inorganic chemistry.",
    ),
    Subject.BIOLOGY: SubjectProfile(
        Subject.BIOLOGY,
        "Biology",
        "Biological concepts, processes and terminology.",
    ),
    Subject.HISTORY: SubjectProfile(
        Subject.HISTORY,
        "History",
        "Historical events, chronology, causes and consequences.",
    ),
    Subject.CIVICS: SubjectProfile(
        Subject.CIVICS,
        "Civics",
        "Constitution, government, rights and political systems.",
    ),
    Subject.GEOGRAPHY: SubjectProfile(
        Subject.GEOGRAPHY,
        "Geography",
        "Physical, human and Indian geography.",
    ),
    Subject.ENGLISH_GRAMMAR: SubjectProfile(
        Subject.ENGLISH_GRAMMAR,
        "English Grammar",
        "English grammar, usage and language concepts.",
    ),
    Subject.COMPUTER_SCIENCE: SubjectProfile(
        Subject.COMPUTER_SCIENCE,
        "Computer Science",
        "Programming, DSA, systems, databases, networks, AI and software development.",
    ),
    Subject.ENGINEERING_MATHEMATICS: SubjectProfile(
        Subject.ENGINEERING_MATHEMATICS,
        "Engineering Mathematics",
        "Engineering-level mathematics and mathematical problem solving.",
    ),
    Subject.DIGITAL_LOGIC: SubjectProfile(
        Subject.DIGITAL_LOGIC,
        "Digital Logic",
        "Digital circuits, Boolean algebra, logic gates and related concepts.",
    ),
    Subject.GENERAL: SubjectProfile(
        Subject.GENERAL,
        "General",
        "General educational topics.",
    ),
}


def get_subject_profile(subject: Subject) -> SubjectProfile:
    """Return the profile for a subject."""
    return SUBJECT_PROFILES[subject]
