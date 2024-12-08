import sqlite3
import json

# Database file name
DB_FILE = "db.sqlite"

# JSON file containing the example orders
JSON_FILE = "example_orders.json"

# Create and populate the database
def initialize_database():
    # Connect to SQLite database (it creates the file if it doesn't exist)
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Create customers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL UNIQUE
    );
    """)

    # Create items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL
    );
    """)

    # Create orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        cust_id INTEGER NOT NULL,
        notes TEXT,
        FOREIGN KEY (cust_id) REFERENCES customers (id)
    );
    """)

    # Create item_list table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS item_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (item_id) REFERENCES items (id)
    );
    """)

    # Load data from JSON file
    try:
        with open(JSON_FILE, 'r') as file:
            orders_data = json.load(file)

        # Insert customers, items, orders, and item_list data
        for order in orders_data:
            # Insert customer if not already present
            cursor.execute("""
            INSERT OR IGNORE INTO customers (name, phone)
            VALUES (?, ?);
            """, (order["name"], order["phone"]))

            # Get customer ID
            cursor.execute("SELECT id FROM customers WHERE phone = ?;", (order["phone"],))
            customer_id = cursor.fetchone()[0]

            # Insert order
            cursor.execute("""
            INSERT INTO orders (timestamp, cust_id, notes)
            VALUES (?, ?, ?);
            """, (order["timestamp"], customer_id, order.get("notes", "")))

            # Get order ID
            cursor.execute("SELECT id FROM orders ORDER BY id DESC LIMIT 1;")
            order_id = cursor.fetchone()[0]

            # Insert items and item_list
            for item in order["items"]:
                # Insert item if not already present
                cursor.execute("""
                INSERT OR IGNORE INTO items (name, price)
                VALUES (?, ?);
                """, (item["name"], item["price"]))

                # Get item ID
                cursor.execute("SELECT id FROM items WHERE name = ?;", (item["name"],))
                item_id = cursor.fetchone()[0]

                # Link item to order
                cursor.execute("""
                INSERT INTO item_list (order_id, item_id)
                VALUES (?, ?);
                """, (order_id, item_id))

        # Commit changes and close the connection
        connection.commit()
        print("Database initialized successfully with data from example_orders.json.")
    except FileNotFoundError:
        print(f"Error: {JSON_FILE} not found.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode {JSON_FILE}. Ensure it is a valid JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    initialize_database()
