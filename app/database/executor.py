from typing import Any

from app.database.connection import get_connection


MAX_ROWS = 100


def execute_query(sql: str) -> list[dict[str, Any]]:
    """Execute validated read-only SQL and return structured rows."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(sql)

        rows = cursor.fetchmany(MAX_ROWS)

        return [
            dict(row)
            for row in rows
        ]

    finally:
        connection.close()
