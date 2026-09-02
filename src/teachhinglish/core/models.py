from enum import Enum

from pydantic import BaseModel, Field


class Subject(str, Enum):
    PHYSICS = "physics"
    MATHEMATICS = "mathematics"
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"
    HISTORY = "history"
    CIVICS = "civics"
    GEOGRAPHY = "geography"
    ENGLISH_GRAMMAR = "english_grammar"
    COMPUTER_SCIENCE = "computer_science"
    ENGINEERING_MATHEMATICS = "engineering_mathematics"
    DIGITAL_LOGIC = "digital_logic"
    GENERAL = "general"


class EducationLevel(str, Enum):
    CLASS_6 = "class_6"
    CLASS_7 = "class_7"
    CLASS_8 = "class_8"
    CLASS_9 = "class_9"
    CLASS_10 = "class_10"
    CLASS_11 = "class_11"
    CLASS_12 = "class_12"

    JEE = "jee"
    NEET = "neet"
    GATE = "gate"

    BTECH = "btech"
    MTECH = "mtech"
    UNIVERSITY = "university"
    PROFESSIONAL = "professional"
    GENERAL = "general"


class Language(str, Enum):
    HINGLISH = "hinglish"
    HINDI = "hindi"
    ENGLISH = "english"


class TeachingStyle(str, Enum):
    CONCEPTUAL = "conceptual"
    EXAM_FOCUSED = "exam_focused"
    DEEP_THEORY = "deep_theory"
    CONVERSATIONAL = "conversational"


class TeachingRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500)
    subject: Subject
    education_level: EducationLevel
    exam_goal: str | None = Field(default=None, max_length=200)
    language: Language = Language.HINGLISH
    style: TeachingStyle = TeachingStyle.CONCEPTUAL

    def clean_topic(self) -> str:
        return self.topic.strip()

class TeachingResponse(BaseModel):
    topic: str
    subject: Subject
    education_level: EducationLevel
    exam_goal: str | None
    language: Language
    style: TeachingStyle
    teaching_script: str