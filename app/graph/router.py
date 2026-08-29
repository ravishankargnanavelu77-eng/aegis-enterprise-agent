from typing import Literal

from app.graph.state import AgentState


def route_task(
    state: AgentState,
) -> Literal["sql_agent", "rag_agent", "research_agent", "end"]:
    """Route the current task to the correct specialized agent."""

    current_task = state.get("current_task")

    if not current_task:
        return "end"

    agent = current_task.get("agent")

    routes = {
        "sql": "sql_agent",
        "rag": "rag_agent",
        "research": "research_agent",
    }

    return routes.get(agent, "end")
