from app.database.inspector import get_database_schema
from app.services.llm import get_llm


def generate_sql(task: str) -> str:
    """Generate a read-only SQLite query for an analytics task."""

    schema = get_database_schema()

    llm = get_llm()

    prompt = f"""
You are an expert enterprise data analyst.

Generate a SQLite SQL query to answer the analytics task.

DATABASE SCHEMA:
{schema}

TASK:
{task}

STRICT RULES:
- Return ONLY valid SQLite SQL.
- Return exactly ONE SQL statement.
- Only use SELECT queries.
- Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, ATTACH, PRAGMA, or other write/admin operations.
- Use only tables and columns present in the provided schema.
- Prefer clear aliases and readable SQL.
- Do not use Markdown.
- Do not explain the query.

SQL:
"""

    response = llm.invoke(prompt)

    content = response.content

    # Gemini may return structured content as a list.
    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))

        content = "".join(text_parts)

    return str(content).strip()
