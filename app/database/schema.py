from app.database.connection import get_connection


def create_schema() -> None:
    """Create the enterprise analytics database schema."""

    connection = get_connection()

    cursor = connection.cursor()

    cursor.executescript(
        """
        DROP TABLE IF EXISTS revenue;

        DROP TABLE IF EXISTS customers;

        DROP TABLE IF EXISTS products;

        DROP TABLE IF EXISTS regions;


        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            segment TEXT NOT NULL,
            industry TEXT NOT NULL
        );


        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL
        );


        CREATE TABLE regions (
            region_id INTEGER PRIMARY KEY,
            region_name TEXT NOT NULL
        );


        CREATE TABLE revenue (
            revenue_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            region_id INTEGER NOT NULL,
            revenue_date TEXT NOT NULL,
            amount REAL NOT NULL,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id),

            FOREIGN KEY (product_id)
                REFERENCES products(product_id),

            FOREIGN KEY (region_id)
                REFERENCES regions(region_id)
        );
        """
    )

    connection.commit()
    connection.close()
