from app.database.connection import get_connection


def get_database_schema() -> str:
    """Return a human-readable representation of the database schema."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    )

    tables = [row["name"] for row in cursor.fetchall()]

    schema_parts = []

    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")

        columns = cursor.fetchall()

        column_lines = []

        for column in columns:
            column_lines.append(
                f"  - {column['name']} ({column['type']})"
            )

        schema_parts.append(
            f"TABLE: {table}\n"
            + "\n".join(column_lines)
        )

    connection.close()

    return "\n\n".join(schema_parts)
