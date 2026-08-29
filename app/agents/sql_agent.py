from app.database.executor import execute_query
from app.database.sql_generator import generate_sql
from app.database.sql_validator import (
    SQLValidationError,
    validate_sql,
)
from app.graph.state import AgentState


def sql_agent_node(state: AgentState) -> dict:
    """Execute a real SQL analytics task."""

    task = state["current_task"]

    print(f"\n[SQL AGENT] Executing: {task['description']}")

    results = dict(state.get("agent_results", {}))

    try:
        generated_sql = generate_sql(task["description"])

        print("\n[SQL AGENT] Generated SQL:")
        print(generated_sql)

        validated_sql = validate_sql(generated_sql)

        rows = execute_query(validated_sql)

        results[task["id"]] = {
            "agent": "sql",
            "status": "completed",
            "task": task["description"],
            "sql": validated_sql,
            "rows": rows,
            "row_count": len(rows),
        }

    except SQLValidationError as error:
        results[task["id"]] = {
            "agent": "sql",
            "status": "failed",
            "task": task["description"],
            "error": f"SQL validation failed: {error}",
        }

    except Exception as error:
        results[task["id"]] = {
            "agent": "sql",
            "status": "failed",
            "task": task["description"],
            "error": str(error),
        }

    return {
        "agent_results": results
    }
