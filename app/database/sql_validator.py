import re


FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "REPLACE",
    "ATTACH",
    "DETACH",
    "PRAGMA",
    "VACUUM",
    "REINDEX",
}


class SQLValidationError(ValueError):
    """Raised when SQL fails safety validation."""


def validate_sql(sql: str) -> str:
    """Validate that SQL is a single read-only SELECT statement."""

    cleaned_sql = sql.strip()

    if not cleaned_sql:
        raise SQLValidationError("SQL query is empty.")

    # Remove one optional trailing semicolon.
    sql_without_trailing_semicolon = cleaned_sql.rstrip(";").strip()

    if not sql_without_trailing_semicolon:
        raise SQLValidationError("SQL query is empty.")

    # Reject multiple statements.
    if ";" in sql_without_trailing_semicolon:
        raise SQLValidationError(
            "Multiple SQL statements are not allowed."
        )

    # Only SELECT or WITH ... SELECT queries are allowed.
    normalized = sql_without_trailing_semicolon.upper()

    if not (
        normalized.startswith("SELECT")
        or normalized.startswith("WITH")
    ):
        raise SQLValidationError(
            "Only read-only SELECT queries are allowed."
        )

    # Reject forbidden keywords.
    for keyword in FORBIDDEN_KEYWORDS:
        pattern = rf"\b{keyword}\b"

        if re.search(pattern, normalized):
            raise SQLValidationError(
                f"Forbidden SQL operation detected: {keyword}"
            )

    return sql_without_trailing_semicolon + ";"
