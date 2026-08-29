from app.database.connection import get_connection


def seed_database() -> None:
    """Insert realistic enterprise analytics data."""

    connection = get_connection()

    cursor = connection.cursor()

    customers = [
        (1, "Apex Industries", "Enterprise", "Manufacturing"),
        (2, "Vertex Financial", "Enterprise", "Financial Services"),
        (3, "Nova Healthcare", "Enterprise", "Healthcare"),
        (4, "Orion Retail Group", "Mid-Market", "Retail"),
        (5, "Titan Technologies", "Enterprise", "Technology"),
        (6, "BlueSky Logistics", "Mid-Market", "Logistics"),
    ]

    products = [
        (1, "Aegis Analytics", "Analytics"),
        (2, "Aegis Cloud", "Cloud"),
        (3, "Aegis Security", "Security"),
    ]

    regions = [
        (1, "North America"),
        (2, "EMEA"),
        (3, "APAC"),
    ]

    cursor.executemany(
        """
        INSERT INTO customers
        (customer_id, customer_name, segment, industry)
        VALUES (?, ?, ?, ?)
        """,
        customers,
    )

    cursor.executemany(
        """
        INSERT INTO products
        (product_id, product_name, category)
        VALUES (?, ?, ?)
        """,
        products,
    )

    cursor.executemany(
        """
        INSERT INTO regions
        (region_id, region_name)
        VALUES (?, ?)
        """,
        regions,
    )

    revenue_data = [
        # Q1
        (1, 1, 1, 1, "2026-01-15", 150000),
        (2, 2, 2, 1, "2026-02-10", 180000),
        (3, 3, 3, 2, "2026-03-05", 160000),
        (4, 4, 1, 3, "2026-03-20", 90000),
        (5, 5, 2, 1, "2026-03-25", 200000),
        (6, 6, 1, 2, "2026-02-18", 80000),

        # Q2 - decline
        (7, 1, 1, 1, "2026-04-15", 120000),
        (8, 2, 2, 1, "2026-05-10", 140000),
        (9, 3, 3, 2, "2026-06-05", 100000),
        (10, 4, 1, 3, "2026-06-20", 85000),
        (11, 5, 2, 1, "2026-06-25", 130000),
        (12, 6, 1, 2, "2026-05-18", 70000),
    ]

    cursor.executemany(
        """
        INSERT INTO revenue
        (
            revenue_id,
            customer_id,
            product_id,
            region_id,
            revenue_date,
            amount
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        revenue_data,
    )

    connection.commit()
    connection.close()
