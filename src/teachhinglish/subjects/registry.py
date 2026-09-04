from dataclasses import dataclass

from teachhinglish.core.models import Subject


@dataclass(frozen=True)
class SubjectProfile:
    subject: Subject
    display_name: str
    description: str
    teaching_approach: str
    required_elements: tuple[str, ...]


SUBJECT_PROFILES: dict[Subject, SubjectProfile] = {
    Subject.PHYSICS: SubjectProfile(
        Subject.PHYSICS,
        "Physics",
        "Physics concepts, numericals, derivations and problem solving.",
        "concepts, physical intuition, laws, derivations, formulas and numerical problem solving",
        (
            "concept explanation",
            "physical intuition",
            "formula or equation",
            "assumptions and conditions",
            "worked numerical example",
            "common mistakes",
        ),
    ),
    Subject.MATHEMATICS: SubjectProfile(
        Subject.MATHEMATICS,
        "Mathematics",
        "Mathematical concepts, proofs, formulas and problem solving.",
        "definitions, mathematical reasoning, formulas, proofs and problem solving",
        (
            "definition or foundational concept",
            "mathematical intuition",
            "formula or theorem",
            "derivation or proof when appropriate",
            "worked examples",
            "common mistakes",
        ),
    ),
    Subject.CHEMISTRY: SubjectProfile(
        Subject.CHEMISTRY,
        "Chemistry",
        "Physical, organic and inorganic chemistry.",
        "concepts, reactions, mechanisms, equations, properties and problem solving",
        (
            "concept explanation",
            "chemical principles",
            "equations or reactions when applicable",
            "conditions and exceptions",
            "worked examples",
            "common mistakes",
        ),
    ),
    Subject.BIOLOGY: SubjectProfile(
        Subject.BIOLOGY,
        "Biology",
        "Biological concepts, processes and terminology.",
        "concepts, biological processes, structures, functions and scientific terminology",
        (
            "definition or concept",
            "key terminology",
            "structure and function when applicable",
            "step-by-step biological process",
            "examples or applications",
            "important facts and common misconceptions",
        ),
    ),
    Subject.HISTORY: SubjectProfile(
        Subject.HISTORY,
        "History",
        "Historical events, chronology, causes and consequences.",
        "historical background, chronology, causes, events, consequences and significance",
        (
            "historical background",
            "chronology",
            "causes",
            "major events",
            "consequences",
            "historical significance",
        ),
    ),
    Subject.CIVICS: SubjectProfile(
        Subject.CIVICS,
        "Civics",
        "Constitution, government, rights and political systems.",
        "constitutional concepts, institutions, government, rights, duties and civic systems",
        (
            "definition or constitutional concept",
            "relevant institutions",
            "roles and responsibilities",
            "rights and duties",
            "real-world example",
            "important distinctions and common misconceptions",
        ),
    ),
    Subject.GEOGRAPHY: SubjectProfile(
        Subject.GEOGRAPHY,
        "Geography",
        "Physical, human and Indian geography.",
        "geographical concepts, spatial relationships, physical processes, human patterns and applications",
        (
            "definition or geographical concept",
            "location or spatial context",
            "physical or human processes",
            "causes and effects",
            "examples or case studies",
            "map or spatial interpretation when relevant",
        ),
    ),
    Subject.ENGLISH_GRAMMAR: SubjectProfile(
        Subject.ENGLISH_GRAMMAR,
        "English Grammar",
        "English grammar, usage and language concepts.",
        "grammar rules, sentence structure, usage, examples and error analysis",
        (
            "grammar rule or concept",
            "sentence structure",
            "correct usage examples",
            "incorrect usage examples",
            "exceptions when applicable",
            "common errors",
        ),
    ),
    Subject.COMPUTER_SCIENCE: SubjectProfile(
        Subject.COMPUTER_SCIENCE,
        "Computer Science",
        "Programming, DSA, systems, databases, networks, AI and software development.",
        "concepts, algorithms, data structures, system behavior, implementation and problem solving",
        (
            "concept explanation",
            "key terminology",
            "algorithm or process when applicable",
            "worked example or implementation",
            "complexity or trade-offs when applicable",
            "common mistakes",
        ),
    ),
    Subject.ENGINEERING_MATHEMATICS: SubjectProfile(
        Subject.ENGINEERING_MATHEMATICS,
        "Engineering Mathematics",
        "Engineering-level mathematics and mathematical problem solving.",
        "mathematical theory, formulas, derivations, methods and engineering applications",
        (
            "mathematical foundation",
            "formula or theorem",
            "derivation when appropriate",
            "solution method",
            "worked engineering-oriented example",
            "common mistakes",
        ),
    ),
    Subject.DIGITAL_LOGIC: SubjectProfile(
        Subject.DIGITAL_LOGIC,
        "Digital Logic",
        "Digital circuits, Boolean algebra, logic gates and related concepts.",
        "Boolean algebra, logic gates, truth tables, circuit behavior and digital design",
        (
            "concept explanation",
            "Boolean expression",
            "truth table when applicable",
            "logic gate or circuit representation",
            "worked simplification or circuit example",
            "common mistakes",
        ),
    ),
    Subject.GENERAL: SubjectProfile(
        Subject.GENERAL,
        "General",
        "General educational topics.",
        "clear conceptual explanation, examples and practical understanding",
        (
            "concept explanation",
            "key terminology",
            "basic-to-advanced explanation",
            "practical example",
            "important points",
            "common misconceptions",
        ),
    ),
}


def get_subject_profile(subject: Subject) -> SubjectProfile:
    """Return the profile for a subject."""
    return SUBJECT_PROFILES[subject]