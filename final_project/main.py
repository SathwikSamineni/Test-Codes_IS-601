from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Database connection
def get_db_connection():
    conn = sqlite3.connect("db.sqlite")
    conn.row_factory = sqlite3.Row  # Ensure rows are returned as dictionaries
    return conn

# === SCHEMA DEFINITIONS ===

# Customer schema
class Customer(BaseModel):
    name: str
    phone: str

# Item schema
class Item(BaseModel):
    name: str
    price: float

# Order schema
class Order(BaseModel):
    customer_id: int
    item_id: int
    quantity: int

# === CUSTOMERS CRUD OPERATIONS ===

@app.post("/customers", response_model=dict)
def create_customer(customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", 
                   (customer.name, customer.phone))
    conn.commit()
    conn.close()
    return {"message": "Customer created successfully"}

@app.get("/customers/{id}", response_model=Customer)
def get_customer(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (id,))
    customer = cursor.fetchone()
    conn.close()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return dict(customer)

@app.put("/customers/{id}", response_model=dict)
def update_customer(id: int, customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", 
                   (customer.name, customer.phone, id))
    conn.commit()
    conn.close()
    return {"message": "Customer updated successfully"}

@app.delete("/customers/{id}", response_model=dict)
def delete_customer(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Customer deleted successfully"}

# === ITEMS CRUD OPERATIONS ===

@app.post("/items", response_model=dict)
def create_item(item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", 
                   (item.name, item.price))
    conn.commit()
    conn.close()
    return {"message": "Item created successfully"}

@app.get("/items/{id}", response_model=Item)
def get_item(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (id,))
    item = cursor.fetchone()
    conn.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return dict(item)

@app.put("/items/{id}", response_model=dict)
def update_item(id: int, item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", 
                   (item.name, item.price, id))
    conn.commit()
    conn.close()
    return {"message": "Item updated successfully"}

@app.delete("/items/{id}", response_model=dict)
def delete_item(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Item deleted successfully"}

# === ORDERS CRUD OPERATIONS ===

@app.post("/orders", response_model=dict)
def create_order(order: Order):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (customer_id, item_id, quantity) VALUES (?, ?, ?)", 
        (order.customer_id, order.item_id, order.quantity)
    )
    conn.commit()
    conn.close()
    return {"message": "Order created successfully"}

@app.get("/orders/{id}", response_model=dict)
def get_order(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id = ?", (id,))
    order = cursor.fetchone()
    conn.close()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return dict(order)

@app.put("/orders/{id}", response_model=dict)
def update_order(id: int, order: Order):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE orders SET customer_id = ?, item_id = ?, quantity = ? WHERE id = ?", 
        (order.customer_id, order.item_id, order.quantity, id)
    )
    conn.commit()
    conn.close()
    return {"message": "Order updated successfully"}

@app.delete("/orders/{id}", response_model=dict)
def delete_order(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Order deleted successfully"}
