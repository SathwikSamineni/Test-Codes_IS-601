import sqlite3
import json

# Load the JSON data
with open('example_orders.json', 'r') as file:
    data = json.load(file)

# Connect to the SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()

# Create tables for customers, items, and orders
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL UNIQUE  -- Ensure unique phone numbers
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        UNIQUE(name, price)  -- Ensure unique item entries based on name and price
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        timestamp INTEGER NOT NULL,
        notes TEXT,
        FOREIGN KEY (customer_id) REFERENCES Customers (id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Order_Items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,  -- Store price in Order_Items for each item in the order
        FOREIGN KEY (order_id) REFERENCES Orders (id),
        FOREIGN KEY (item_id) REFERENCES Items (id)
    )
''')

# Insert customers, orders, and order items from JSON data
for order in data:
    customer_name = order['name']
    customer_phone = order['phone']

    # Insert or ignore existing customers based on phone number
    cursor.execute('''
        INSERT OR IGNORE INTO Customers (name, phone) VALUES (?, ?)
    ''', (customer_name, customer_phone))

    # Get the customer ID
    cursor.execute('SELECT id FROM Customers WHERE phone = ?', (customer_phone,))
    customer_id = cursor.fetchone()[0]

    # Insert the order
    timestamp = order['timestamp']
    notes = order.get('notes', '')
    cursor.execute('''
        INSERT INTO Orders (customer_id, timestamp, notes)
        VALUES (?, ?, ?)
    ''', (customer_id, timestamp, notes))

    # Get the order ID
    order_id = cursor.lastrowid

    # Insert items and link them to the order, store the price in the Order_Items table
    for item in order['items']:
        item_name = item['name']
        item_price = item['price']

        # Insert or ignore existing items
        cursor.execute('''
            INSERT OR IGNORE INTO Items (name, price) VALUES (?, ?)
        ''', (item_name, item_price))

        # Get the item ID
        cursor.execute('SELECT id FROM Items WHERE name = ? AND price = ?', (item_name, item_price))
        item_id = cursor.fetchone()[0]

        # Insert the order-item entry with quantity and price in the Order_Items table
        cursor.execute('''
            INSERT INTO Order_Items (order_id, item_id, quantity, price)
            VALUES (?, ?, ?, ?)
        ''', (order_id, item_id, 1, item_price))  # Assuming quantity is 1 for simplicity

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database initialized successfully!")
