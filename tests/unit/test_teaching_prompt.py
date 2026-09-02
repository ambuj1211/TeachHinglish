from teachhinglish.core.models import TeachingRequest
from teachhinglish.prompts.teaching import TeachingPromptBuilder


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
