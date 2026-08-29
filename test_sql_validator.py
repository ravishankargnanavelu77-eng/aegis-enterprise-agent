from app.database.sql_validator import (
    SQLValidationError,
    validate_sql,
)


safe_sql = """
SELECT
    SUM(amount) AS total_revenue
FROM revenue;
"""

dangerous_sql = """
DROP TABLE revenue;
"""


print("--- SAFE QUERY ---")

try:
    print(validate_sql(safe_sql))
except SQLValidationError as error:
    print(f"Rejected: {error}")


print("\n--- DANGEROUS QUERY ---")

try:
    print(validate_sql(dangerous_sql))
except SQLValidationError as error:
    print(f"Rejected: {error}")
