from app.graph.state import AgentState
from app.rag.retriever import retrieve_documents
from app.services.llm import get_llm


def _extract_text(content) -> str:
    """Extract plain text from LLM response content."""

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))

        return "".join(parts).strip()

    return str(content).strip()


def rag_agent_node(state: AgentState) -> dict:
    """Execute an internal knowledge-base RAG task."""

    task = state["current_task"]

    print(f"\n[RAG AGENT] Executing: {task['description']}")

    results = dict(state.get("agent_results", {}))

    try:
        documents = retrieve_documents(
            task["description"],
            k=4,
        )

        print(
            f"[RAG AGENT] Retrieved "
            f"{len(documents)} relevant chunks"
        )

        context_parts = []

        for index, document in enumerate(documents, start=1):
            context_parts.append(
                f"""
SOURCE {index}: {document['source']}

{document['content']}
"""
            )

        context = "\n\n".join(context_parts)

        llm = get_llm()

        prompt = f"""
You are an enterprise business intelligence analyst.

Your job is to analyze INTERNAL company documents.

TASK:
{task['description']}

RETRIEVED INTERNAL EVIDENCE:
{context}

RULES:
- Use only the retrieved evidence.
- Do not invent facts.
- Clearly explain the findings.
- Mention important numbers when present.
- Identify the main internal causes or insights.
- Keep the response concise but useful.
- If evidence is insufficient, explicitly say so.

Return a professional enterprise analysis.
"""

        response = llm.invoke(prompt)

        analysis = _extract_text(response.content)

        sources = list(
            {
                document["source"]
                for document in documents
            }
        )

        results[task["id"]] = {
            "agent": "rag",
            "status": "completed",
            "task": task["description"],
            "analysis": analysis,
            "sources": sources,
            "retrieved_chunks": len(documents),
        }

    except Exception as error:
        results[task["id"]] = {
            "agent": "rag",
            "status": "failed",
            "task": task["description"],
            "error": str(error),
        }

    return {
        "agent_results": results
    }
