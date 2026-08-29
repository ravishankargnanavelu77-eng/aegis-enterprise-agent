from app.database.sql_generator import generate_sql


task = (
    "Compare total revenue in Q1 and Q2 of 2026 "
    "and calculate the percentage change."
)

sql = generate_sql(task)

print("\n--- GENERATED SQL ---\n")
print(sql)
