from typing import Annotated, Any

from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    """Shared state that flows through the Aegis agent graph."""

    # User request
    query: str

    # Conversation / agent messages
    messages: Annotated[list, add_messages]

    # Execution planning
    execution_plan: list[dict[str, Any]]

    # Task execution
    current_task: dict[str, Any]
    task_index: int

    # Agent outputs
    agent_results: dict[str, Any]

    # Evidence collected from all agents
    evidence: list[dict[str, Any]]

    # Final generated response
    final_answer: str

    # Validation and retry handling
    validation_result: dict[str, Any]
    retry_count: int

    # Error tracking
    errors: list[str]
