from teachhinglish.core.models import TeachingRequest
from teachhinglish.prompts.teaching import TeachingPromptBuilder
from teachhinglish.core.plan import TeachingPlan

def test_school_prompt_uses_school_greeting():
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    prompt = TeachingPromptBuilder().build(request, "Physics context")

    assert "Hello bachcho" in prompt
    assert "good morning" in prompt
    assert "good afternoon" in prompt
    assert "good evening" in prompt
    assert "please subscribe" in prompt
    assert "To chaliye shuru karte hain" in prompt


def test_btech_prompt_uses_friends_greeting():
    request = TeachingRequest(
        topic="Binary Search Tree",
        subject="computer_science",
        education_level="btech",
        exam_goal="semester",
    )

    prompt = TeachingPromptBuilder().build(request, "CSE context")

    assert "Hello friends, vaste gunna huiyan" in prompt

    greeting_section = prompt.split("OPENING STYLE", 1)[1].split(
        "TEACHING REQUIREMENTS", 1
    )[0]

    assert "Hello friends, vaste gunna huiyan" in greeting_section
    assert "hello bachcho" not in greeting_section.lower()


def test_gate_prompt_uses_friends_greeting():
    request = TeachingRequest(
        topic="Operating Systems",
        subject="computer_science",
        education_level="gate",
        exam_goal="gate",
    )

    prompt = TeachingPromptBuilder().build(request, "OS context")

    assert "Hello friends, vaste gunna huiyan" in prompt

    greeting_section = prompt.split("OPENING STYLE", 1)[1].split(
        "TEACHING REQUIREMENTS", 1
    )[0]

    assert "Hello friends, vaste gunna huiyan" in greeting_section
    assert "hello bachcho" not in greeting_section.lower()


def test_prompt_contains_student_context():
    request = TeachingRequest(
        topic="Transformer Architecture",
        subject="computer_science",
        education_level="mtech",
        exam_goal="advanced_learning",
    )

    prompt = TeachingPromptBuilder().build(request, "Attention mechanisms")

    assert "Transformer Architecture" in prompt
    assert "computer_science" in prompt
    assert "mtech" in prompt
    assert "advanced_learning" in prompt
    assert "Attention mechanisms" in prompt

def test_prompt_contains_teaching_plan():
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    plan = TeachingPlan(
        learning_objectives=["Understand the relationship between force and acceleration."],
        prerequisites=["Basic understanding of force and mass."],
        concepts=["Newton's Second Law"],
        examples=["A 10 N force acting on a 2 kg mass."],
        teaching_sequence=[
            "Introduce the law.",
            "Explain F = ma.",
            "Solve a numerical example.",
        ],
    )

    prompt = TeachingPromptBuilder().build(
        request,
        "Physics context",
        plan,
    )

    assert "LEARNING OBJECTIVES" in prompt
    assert "Understand the relationship between force and acceleration." in prompt
    assert "Basic understanding of force and mass." in prompt
    assert "Newton's Second Law" in prompt
    assert "A 10 N force acting on a 2 kg mass." in prompt
    assert "Explain F = ma." in prompt

def test_prompt_contains_subject_teaching_guidance():
    request = TeachingRequest(
        topic="Newton's Second Law",
        subject="physics",
        education_level="class_11",
        exam_goal="jee",
    )

    prompt = TeachingPromptBuilder().build(request, "Physics context")

    assert "SUBJECT TEACHING GUIDANCE" in prompt
    assert "physical intuition" in prompt
    assert "formula or equation" in prompt
    assert "worked numerical example" in prompt
    assert "common mistakes" in prompt

def test_prompt_uses_subject_specific_guidance():
    request = TeachingRequest(
        topic="Indian Independence Movement",
        subject="history",
        education_level="class_10",
        exam_goal="school",
    )

    prompt = TeachingPromptBuilder().build(request, "History context")

    assert "chronology" in prompt
    assert "historical background" in prompt
    assert "major events" in prompt
    assert "consequences" in prompt