from app.services.llm import get_llm
from app.services.research import search_web


RESEARCH_SYSTEM_PROMPT = """
You are an Enterprise Market Research Agent.

Your job is to analyze external market information relevant to a business question.

You must:

1. Identify important external trends.
2. Identify macroeconomic or industry factors.
3. Identify competitive dynamics when evidence is available.
4. Distinguish evidence from inference.
5. Do not invent facts.
6. Base conclusions only on the supplied research sources.
7. Clearly explain how external factors may affect the business problem.

Provide a structured executive-ready analysis with:

- Executive Summary
- Key External Market Trends
- Potential Business Impact
- Evidence-Based Findings
- Risks and Uncertainty
"""


def run_research_agent(task: str) -> dict:
    """Execute external web research for a planner task."""

    search_results = search_web(
        query=task,
        max_results=5,
    )

    if not search_results:
        return {
            "agent": "research",
            "status": "completed",
            "task": task,
            "analysis": "No external research results were found.",
            "sources": [],
        }

    research_context = "\n\n".join(
        [
            (
                f"SOURCE {index}\n"
                f"TITLE: {result['title']}\n"
                f"URL: {result['url']}\n"
                f"CONTENT:\n{result['content']}"
            )
            for index, result in enumerate(search_results, start=1)
        ]
    )

    prompt = f"""
{RESEARCH_SYSTEM_PROMPT}

TASK:
{task}

EXTERNAL RESEARCH SOURCES:

{research_context}

Analyze the sources and produce an enterprise research report.
Do not claim information that is not supported by the sources.
"""

    llm = get_llm()

    response = llm.invoke(prompt)

    return {
        "agent": "research",
        "status": "completed",
        "task": task,
        "analysis": response.content,
        "sources": [
            {
                "title": result["title"],
                "url": result["url"],
            }
            for result in search_results
        ],
        "source_count": len(search_results),
    }


def research_agent_node(state: dict) -> dict:
    """LangGraph node for executing the Research Agent."""

    current_task = state.get("current_task", {})

    task_id = current_task.get("id")
    task_description = current_task.get("description", "")

    print(f"\n[RESEARCH AGENT] Processing {task_id}")
    print(f"[RESEARCH AGENT] Task: {task_description}")

    try:
        result = run_research_agent(task_description)

        print(
            f"[RESEARCH AGENT] Completed {task_id} "
            f"with {result.get('source_count', 0)} sources"
        )

    except Exception as error:

        print(
            f"[RESEARCH AGENT] Failed {task_id}: {error}"
        )

        result = {
            "agent": "research",
            "status": "failed",
            "task": task_description,
            "error": str(error),
            "analysis": "",
            "sources": [],
            "source_count": 0,
        }

    agent_results = dict(state.get("agent_results", {}))

    agent_results[task_id] = result

    return {
        "agent_results": agent_results
    }
