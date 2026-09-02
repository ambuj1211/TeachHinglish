from langgraph.graph import END, START, StateGraph

from teachhinglish.graph.knowledge import load_knowledge
from teachhinglish.graph.planner import plan_teaching
from teachhinglish.graph.prompt import build_teaching_prompt
from teachhinglish.graph.state import TeachingState
from teachhinglish.graph.teacher import generate_teaching_script
from teachhinglish.graph.validator import validate_teaching_script


def _validation_route(state: TeachingState) -> str:
    if state.validation_passed:
        return "end"

    return "retry"


def build_teaching_graph():
    graph = StateGraph(TeachingState)

    graph.add_node("planner", plan_teaching)
    graph.add_node("knowledge", load_knowledge)
    graph.add_node("prompt", build_teaching_prompt)
    graph.add_node("teacher", generate_teaching_script)
    graph.add_node("validator", validate_teaching_script)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "knowledge")
    graph.add_edge("knowledge", "prompt")
    graph.add_edge("prompt", "teacher")
    graph.add_edge("teacher", "validator")

    graph.add_conditional_edges(
        "validator",
        _validation_route,
        {
            "retry": "teacher",
            "end": END,
        },
    )

    return graph.compile()