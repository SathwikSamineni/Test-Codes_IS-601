from fastapi import FastAPI, HTTPException

app = FastAPI()

customers = [
    {"id": 0, "phone": "609-555-0124", "name": "Karl"},
    {"id": 1, "phone": "609-555-1234", "name": "Mike"},
    {"id": 3, "phone": "609-555-4302", "name": "Ryan"},
    {"id": 5, "phone": "609-555-4111", "name": "Sathwik"},
    {"id": 7, "phone": "609-555-5098", "name": "Mathew Toegel"},
]


@app.get("/customers/{id}")
def get_customer(id: int):
    
    for customer in customers:
        if customer["id"] == id:
            return customer

    raise HTTPException(status_code=404, detail="Customer not found")
