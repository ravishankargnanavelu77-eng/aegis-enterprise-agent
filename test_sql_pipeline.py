from app.database.executor import execute_query
from app.database.sql_generator import generate_sql
from app.database.sql_validator import validate_sql


task = (
    "Compare total revenue in Q1 and Q2 of 2026 "
    "and calculate the percentage change."
)

print("\n--- TASK ---")
print(task)

sql = generate_sql(task)

print("\n--- GENERATED SQL ---")
print(sql)

validated_sql = validate_sql(sql)

print("\n--- VALIDATED SQL ---")
print(validated_sql)

rows = execute_query(validated_sql)

print("\n--- QUERY RESULTS ---")

for row in rows:
    print(row)
