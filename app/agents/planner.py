from pydantic import BaseModel, Field

from app.services.llm import get_llm, invoke_with_retry


class AgentTask(BaseModel):
    """A task assigned to a specialized agent."""

    id: str = Field(description="Unique task identifier")

    agent: str = Field(
        description=(
            "Agent that should execute the task. "
            "Must be one of: sql, rag, research."
        )
    )

    description: str = Field(
        description="Clear description of the task to execute"
    )


class ExecutionPlan(BaseModel):
    """Structured execution plan created by the planner."""

    goal: str = Field(
        description="Overall goal of the user query"
    )

    tasks: list[AgentTask] = Field(
        description="Ordered list of specialized tasks"
    )


def create_execution_plan(query: str) -> ExecutionPlan:
    """Use the LLM to break a complex query into specialized tasks."""

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        ExecutionPlan
    )

    prompt = f"""
You are the planning agent for an enterprise AI system.

Analyze the user's query and break it into the minimum number
of useful tasks.

Available agents:

1. sql
   Use for structured database analysis, metrics, trends,
   aggregations, and numerical analysis.

2. rag
   Use for searching and analyzing internal enterprise documents.

3. research
   Use for external market research and publicly available information.

Rules:
- Only create tasks that are necessary.
- Use one or more of the available agents.
- Do not answer the user's question.
- Create clear, specific tasks.
- Prefer parallel tasks when they are independent.

User query:
{query}
"""

    return invoke_with_retry(
        runnable=structured_llm,
        prompt=prompt,
    )
