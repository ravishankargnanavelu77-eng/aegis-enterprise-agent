from app.database.inspector import get_database_schema


schema = get_database_schema()

print("\n--- DATABASE SCHEMA ---\n")
print(schema)
