from app.database.schema import create_schema
from app.database.seed import seed_database


def main() -> None:
    create_schema()
    seed_database()

    print("Enterprise database created successfully.")


if __name__ == "__main__":
    main()
