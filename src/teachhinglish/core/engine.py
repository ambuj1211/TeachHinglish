from teachhinglish.core.models import TeachingRequest, TeachingResponse
from teachhinglish.graph.state import TeachingState
from teachhinglish.graph.workflow import build_teaching_graph


class TeacherLanguageEngine:
    """Coordinates the complete TeachHinglish teaching workflow."""

    def __init__(self) -> None:
        self.graph = build_teaching_graph()

    async def teach(
        self,
        request: TeachingRequest,
    ) -> TeachingResponse:
        """Generate a complete validated teaching script."""

        state = TeachingState(request=request)

        final_state = await self.graph.ainvoke(state)

        return TeachingResponse(
            topic=request.topic,
            subject=request.subject,
            education_level=request.education_level,
            exam_goal=request.exam_goal,
            language=request.language,
            style=request.style,
            teaching_script=final_state["teaching_script"],
        )