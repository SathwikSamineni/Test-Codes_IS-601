from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
from datetime import datetime
import sqlite3

app = FastAPI()

# Database helper functions
def get_db_connection():
    conn = sqlite3.connect("db.sqlite")
    conn.row_factory = sqlite3.Row
    return conn

# Pydantic models for POST and PUT requests
class Customer(BaseModel):
    name: str
    phone: str

class Item(BaseModel):
    name: str
    price: float

class OrderItem(BaseModel):
    item_name: str
    quantity: int

class OrderRequest(BaseModel):
    customer_name: str
    phone: str
    items: List[OrderItem]
    notes: str

# --- GET Endpoints ---
@app.get("/customers")
def get_customers(limit: int = Query(10, description="Number of customers to retrieve"), offset: int = 0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers LIMIT ? OFFSET ?", (limit, offset))
    customers = cursor.fetchall()
    conn.close()
    return {"customers": [{"id": row[0], "name": row[1], "phone": row[2]} for row in customers]}

@app.get("/items")
def get_items(limit: int = 10, offset: int = 0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items LIMIT ? OFFSET ?", (limit, offset))
    items = cursor.fetchall()
    conn.close()
    return {"items": [{"id": row[0], "name": row[1], "price": row[2]} for row in items]}

@app.get("/orders")
def get_orders(limit: int = 10, offset: int = 0):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch orders with a limit and offset
    cursor.execute("SELECT * FROM orders LIMIT ? OFFSET ?", (limit, offset))
    orders = cursor.fetchall()
    
    order_list = []
    for order in orders:
        customer_id = order[1]
        
        # Fetch customer details
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        customer = cursor.fetchone()
        
        # Fetch order items with their details (including price)
        items = []
        cursor.execute(""" 
            SELECT oi.item_id, i.name, oi.quantity, oi.price 
            FROM Order_Items oi 
            JOIN items i ON oi.item_id = i.id 
            WHERE oi.order_id = ?
        """, (order[0],))
        order_items = cursor.fetchall()
        
        for order_item in order_items:
            items.append({
                "item_id": order_item[0],
                "item_name": order_item[1],
                "quantity": order_item[2],
                "price": order_item[3]  # Add price to the item details
            })
        
        # Construct the order object
        order_list.append({
            "id": order[0],
            "customer_id": customer_id,
            "customer_name": customer[1],  # Customer name
            "phone": customer[2],         # Customer phone
            "notes": order[3],            # Order notes
            "items": items                # Order items with details
        })
    
    conn.close()
    return {"orders": order_list}

# --- Filter Endpoints ---
@app.get("/customers/filter")
def filter_customers(name: str = Query(None, description="Filter customers by name")):
    if name is None:
        raise HTTPException(status_code=400, detail="Name parameter is required.")
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE name LIKE ? COLLATE NOCASE", (f"%{name}%",))
    customers = cursor.fetchall()
    conn.close()

    if not customers:
        raise HTTPException(status_code=404, detail="No customers found.")

    return {"customers": [{"id": row[0], "name": row[1], "phone": row[2]} for row in customers]}

@app.get("/items/filter")
def filter_items(min_price: float = Query(0), max_price: float = Query(100)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE price BETWEEN ? AND ?", (min_price, max_price))
    items = cursor.fetchall()
    conn.close()
    
    if not items:
        raise HTTPException(status_code=404, detail="No items found in this price range.")

    return {"items": [{"id": row[0], "name": row[1], "price": row[2]} for row in items]}

@app.get("/orders/filter")
def filter_orders(customer_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,))
    orders = cursor.fetchall()

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this customer.")

    order_list = []
    for order in orders:
        cursor.execute("SELECT oi.item_id, i.name, oi.quantity, oi.price FROM Order_Items oi JOIN items i ON oi.item_id = i.id WHERE oi.order_id = ?", (order[0],))
        order_items = cursor.fetchall()
        
        items = []
        for order_item in order_items:
            items.append({
                "item_id": order_item[0],
                "item_name": order_item[1],
                "quantity": order_item[2],
                "price": order_item[3]
            })

        order_list.append({
            "id": order[0],
            "customer_id": order[1],
            "items": items
        })

    conn.close()
    return {"orders": order_list}

# --- POST Endpoints ---
@app.post("/customers")
def create_customer(customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone))
    conn.commit()
    conn.close()
    return {"message": "Customer created successfully"}

@app.post("/items")
def create_item(item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
    conn.commit()
    conn.close()
    return {"message": "Item created successfully"}

@app.post("/orders")
def create_order(order: OrderRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if customer exists, if not, create
    cursor.execute("SELECT id FROM customers WHERE phone = ?", (order.phone,))
    customer = cursor.fetchone()
    if not customer:
        cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", 
                       (order.customer_name, order.phone))
        customer_id = cursor.lastrowid
    else:
        customer_id = customer["id"]

    # Create the order
    timestamp = int(datetime.utcnow().timestamp())
    cursor.execute("INSERT INTO orders (customer_id, timestamp, notes) VALUES (?, ?, ?)", 
                   (customer_id, timestamp, order.notes))
    order_id = cursor.lastrowid

    # Add items to the order (no price option)
    for order_item in order.items:
        cursor.execute("SELECT id FROM items WHERE name = ?", (order_item.item_name,))
        item = cursor.fetchone()
        if not item:
            raise HTTPException(status_code=404, detail=f"Item '{order_item.item_name}' not found")
        item_id = item["id"]
        cursor.execute("INSERT INTO Order_Items (order_id, item_id, quantity) VALUES (?, ?, ?)", 
                       (order_id, item_id, order_item.quantity))

    conn.commit()
    return {"order_id": order_id, "message": "Order created successfully"}

# --- PUT Endpoints ---
@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", (customer.name, customer.phone, customer_id))
    conn.commit()
    conn.close()
    return {"message": "Customer updated successfully"}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (item.name, item.price, item_id))
    conn.commit()
    conn.close()
    return {"message": "Item updated successfully"}

@app.put("/orders/{order_id}")
def update_order(order_id: int, order: OrderRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the order exists
    cursor.execute("SELECT id FROM orders WHERE id = ?", (order_id,))
    existing_order = cursor.fetchone()
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update order details
    cursor.execute(""" 
        UPDATE orders 
        SET notes = ? 
        WHERE id = ? 
    """, (order.notes, order_id))

    # Delete existing order items
    cursor.execute("DELETE FROM Order_Items WHERE order_id = ?", (order_id,))

    # Add the new items for the order (no price option)
    for order_item in order.items:
        cursor.execute("SELECT id FROM items WHERE name = ?", (order_item.item_name,))
        item = cursor.fetchone()
        if not item:
            raise HTTPException(status_code=404, detail=f"Item '{order_item.item_name}' not found")
        item_id = item["id"]
        cursor.execute("INSERT INTO Order_Items (order_id, item_id, quantity) VALUES (?, ?, ?)", 
                       (order_id, item_id, order_item.quantity))

    conn.commit()
    conn.close()
    return {"message": "Order updated successfully"}

# --- DELETE Endpoints ---
@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()
    return {"message": "Customer deleted successfully"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return {"message": "Item deleted successfully"}

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    return {"message": "Order deleted successfully"}
