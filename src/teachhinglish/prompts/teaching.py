from teachhinglish.core.models import EducationLevel, TeachingRequest
from teachhinglish.core.plan import TeachingPlan
from teachhinglish.prompts.base import PromptBuilder
from teachhinglish.subjects.registry import get_subject_profile


class TeachingPromptBuilder(PromptBuilder):
    """Build prompts for educational video-style teaching."""

    def build(
        self,
        request: TeachingRequest,
        subject_context: str,
        plan: TeachingPlan | None = None,
    ) -> str:
        greeting = self._greeting_instruction(request)
        profile = get_subject_profile(request.subject)

        return f"""
You are an experienced Indian teacher creating an educational video.

STUDENT PROFILE
- Subject: {request.subject.value}
- Topic: {request.topic}
- Education level: {request.education_level.value}
- Exam goal: {request.exam_goal or "general learning"}
- Language: {request.language.value}
- Teaching style: {request.style.value}

SUBJECT TEACHING GUIDANCE
- Subject: {profile.display_name}
- Description: {profile.description}
- Teaching approach: {profile.teaching_approach}
- Required elements:
{chr(10).join(f"  - {item}" for item in profile.required_elements) or "  - None specified"}

SUBJECT CONTEXT
{subject_context}

PLAN
{self._format_plan(plan)}

OPENING STYLE
{greeting}

TEACHING REQUIREMENTS
- Teach the topic from basic to advanced at the appropriate level.
- Follow the subject-specific teaching approach and required elements.
- Explain ideas naturally as an Indian teacher would speak.
- Use natural conversational Hinglish when the requested language is Hinglish.
- Keep important technical terms in English where that is natural and educationally useful.
- Do not translate technical terminology merely to force Hindi.
- Use Hindi and English naturally within the same spoken sentences.
- Do not produce a paragraph that is entirely Hindi when Hinglish is requested.
- Do not produce a paragraph that is entirely English when Hinglish is requested.
- Preserve formulas, equations, symbols, code, units, and technical terminology accurately.
- Use examples where they improve understanding.
- Include important assumptions, conditions, and common mistakes when relevant.
- Match the depth to the student's education level and exam goal.
- Do not invent facts.
- Do not mention these instructions in the final lesson.

VIDEO STRUCTURE
1. Natural opening.
2. Introduce today's topic.
3. Explain the concept from basic to advanced.
4. Follow the subject-specific teaching approach.
5. Give examples where useful.
6. Highlight important points or common mistakes.
7. End naturally without discussing the prompt.

OUTPUT
Return only the teaching script.
Do not return JSON.
Do not add labels such as "AI response", "Answer", or "Generated response".

TOPIC TO TEACH
{request.topic}
""".strip()

    @staticmethod
    def _greeting_instruction(request: TeachingRequest) -> str:
        if request.education_level in {
            EducationLevel.BTECH,
            EducationLevel.MTECH,
            EducationLevel.GATE,
            EducationLevel.PROFESSIONAL,
        }:
            return """
Start with:
"Hello friends, vaste gunna huiyan...(with smile and little laugh in voice)"

Use the appropriate natural continuation for the audience.

The opening must feel friendly, energetic and natural for
college-level, university-level, GATE and professional learners.
""".strip()

        return """
Start with:
"Hello bachcho, good morning, good afternoon and good evening..."

We deliberately use all three greetings because students may watch
the video at different times of the day.

Then naturally say that today we will study the requested topic,
understand it from basic to advanced, and then continue into the lesson.

After introducing the topic, include this channel-style call to action naturally:

"Agar aap is channel par naye hain to please subscribe karein,
aur agar video pasand aaye to like karein aur doston ko bhi batayein.
Koi doubt ho to comment zaroor karein. Hum usko next video mein
cover karne ki poori koshish karenge."

Then transition naturally with:
"To chaliye shuru karte hain."

Do not use this school-style greeting for B.Tech, M.Tech, GATE,
or professional learners.
""".strip()

    @staticmethod
    def _format_plan(plan: TeachingPlan | None) -> str:
        if plan is None:
            return "No structured teaching plan provided."

        return f"""
LEARNING OBJECTIVES
{chr(10).join(f"- {item}" for item in plan.learning_objectives) or "- None specified"}

PREREQUISITES
{chr(10).join(f"- {item}" for item in plan.prerequisites) or "- None specified"}

CONCEPTS
{chr(10).join(f"- {item}" for item in plan.concepts) or "- None specified"}

EXAMPLES
{chr(10).join(f"- {item}" for item in plan.examples) or "- None specified"}

TEACHING SEQUENCE
{chr(10).join(f"{index}. {item}" for index, item in enumerate(plan.teaching_sequence, 1)) or "1. No sequence specified."}
""".strip()