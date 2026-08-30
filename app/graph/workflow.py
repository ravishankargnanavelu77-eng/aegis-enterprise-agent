from langgraph.graph import END, START, StateGraph

from app.agents.planner import create_execution_plan
from app.agents.rag_agent import rag_agent_node
from app.agents.research_agent import research_agent_node
from app.agents.sql_agent import sql_agent_node
from app.graph.router import route_task
from app.graph.state import AgentState
from app.services.llm import get_llm, invoke_with_retry


def _extract_text(content) -> str:
    """Extract plain text from an LLM response."""

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts = []

        for item in content:
            if (
                isinstance(item, dict)
                and item.get("type") == "text"
            ):
                parts.append(item.get("text", ""))

        return "".join(parts).strip()

    return str(content).strip()


def planner_node(state: AgentState) -> dict:
    """Create an LLM-powered execution plan."""

    query = state["query"]

    print(f"\n[PLANNER] Analyzing query: {query}")

    plan = create_execution_plan(query)

    execution_plan = [
        {
            "id": task.id,
            "agent": task.agent,
            "description": task.description,
        }
        for task in plan.tasks
    ]

    print(f"[PLANNER] Goal: {plan.goal}")
    print(f"[PLANNER] Created {len(execution_plan)} tasks")

    return {
        "execution_plan": execution_plan,
        "task_index": 0,
        "agent_results": {},
    }


def select_task_node(state: AgentState) -> dict:
    """Select the next task from the execution plan."""

    plan = state.get("execution_plan", [])
    task_index = state.get("task_index", 0)

    if task_index >= len(plan):
        print("\n[TASK SELECTOR] No tasks remaining")

        return {
            "current_task": {}
        }

    task = plan[task_index]

    print(
        f"\n[TASK SELECTOR] Selected "
        f"{task['id']} → {task['agent'].upper()}"
    )

    return {
        "current_task": task
    }


def increment_task_node(state: AgentState) -> dict:
    """Move to the next task."""

    current_index = state.get("task_index", 0)

    return {
        "task_index": current_index + 1
    }


def route_after_task(state: AgentState) -> str:
    """Decide whether to execute another task or synthesize."""

    plan = state.get("execution_plan", [])
    task_index = state.get("task_index", 0)

    if task_index >= len(plan):
        return "synthesizer"

    return "select_task"


def synthesizer_node(state: AgentState) -> dict:
    """Synthesize evidence from all specialized agents."""

    query = state.get("query", "")
    results = state.get("agent_results", {})

    print(
        f"\n[SYNTHESIZER] Received "
        f"{len(results)} agent results"
    )

    evidence_parts = []

    for task_id, result in results.items():
        agent = result.get("agent", "unknown")
        status = result.get("status", "unknown")
        task = result.get("task", "")

        evidence_parts.append(
            f"""
==================================================
TASK ID: {task_id}
AGENT: {agent.upper()}
STATUS: {status}

TASK:
{task}

AGENT RESULT:
{result}
==================================================
"""
        )

    evidence = "\n".join(evidence_parts)



    prompt = f"""
You are Aegis, an enterprise AI decision intelligence system.

Your job is to synthesize evidence produced by multiple
specialized AI agents into a professional executive analysis.

ORIGINAL BUSINESS QUESTION:
{query}

AVAILABLE AGENT EVIDENCE:
{evidence}

STRICT RULES:
- Use only facts present in the agent evidence.
- Do not invent numbers, causes, customers, or trends.
- Distinguish between quantitative evidence and qualitative evidence.
- If agents disagree or evidence is incomplete, say so clearly.
- Do not claim external facts unless they are present in the evidence.
- Prioritize concrete findings supported by multiple agents.
- Keep the analysis concise and executive-friendly.

Return the answer using exactly these sections:

## Executive Summary

## Key Findings

## Primary Drivers

## Evidence and Sources

## Recommended Actions

## Confidence and Limitations
"""

    response = invoke_with_retry(get_llm(), prompt)

    final_answer = _extract_text(response.content)

    return {
        "final_answer": final_answer
    }


def build_graph():
    """Build and compile the Aegis multi-agent workflow."""

    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("planner", planner_node)
    graph.add_node("select_task", select_task_node)
    graph.add_node("sql_agent", sql_agent_node)
    graph.add_node("rag_agent", rag_agent_node)
    graph.add_node("research_agent", research_agent_node)
    graph.add_node("increment_task", increment_task_node)
    graph.add_node("synthesizer", synthesizer_node)

    # Start
    graph.add_edge(START, "planner")

    # Planner → first task
    graph.add_edge("planner", "select_task")

    # Task selection → specialized agent
    graph.add_conditional_edges(
        "select_task",
        route_task,
        {
            "sql_agent": "sql_agent",
            "rag_agent": "rag_agent",
            "research_agent": "research_agent",
            "end": "synthesizer",
        },
    )

    # Agents → increment task
    graph.add_edge("sql_agent", "increment_task")
    graph.add_edge("rag_agent", "increment_task")
    graph.add_edge("research_agent", "increment_task")

    # Increment → next task or synthesis
    graph.add_conditional_edges(
        "increment_task",
        route_after_task,
        {
            "select_task": "select_task",
            "synthesizer": "synthesizer",
        },
    )

    # Finish
    graph.add_edge("synthesizer", END)

    return graph.compile()


