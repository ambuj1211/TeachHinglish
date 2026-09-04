from dataclasses import dataclass, field


@dataclass
class TeachingPlan:
    """Structured teaching plan produced before script generation."""

    learning_objectives: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    concepts: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    teaching_sequence: list[str] = field(default_factory=list)