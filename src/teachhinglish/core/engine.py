from teachhinglish.core.models import TeachingRequest, TeachingResponse
from teachhinglish.prompts.base import PromptBuilder
from teachhinglish.providers.base import LLMProvider
from teachhinglish.subjects.registry import get_subject_profile


class TeacherLanguageEngine:
    """Coordinates request, subject context, prompt and LLM generation."""

    def __init__(
        self,
        provider: LLMProvider,
        prompt_builder: PromptBuilder,
    ) -> None:
        self.provider = provider
        self.prompt_builder = prompt_builder

    async def teach(
        self,
        request: TeachingRequest,
    ) -> TeachingResponse:
        """Generate a complete teaching script."""

        subject_profile = get_subject_profile(request.subject)

        subject_context = (
            f"Subject: {subject_profile.display_name}\n"
            f"Description: {subject_profile.description}"
        )

        prompt = self.prompt_builder.build(
            request,
            subject_context,
        )

        teaching_script = await self.provider.generate(
            prompt,
            request.subject,
        )

        return TeachingResponse(
            topic=request.topic,
            subject=request.subject,
            education_level=request.education_level,
            exam_goal=request.exam_goal,
            language=request.language,
            style=request.style,
            teaching_script=teaching_script,
        )