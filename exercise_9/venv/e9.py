from fastapi import FastAPI, HTTPException

# Initialize FastAPI app
app = FastAPI()

# Hardcoded customers list
customers = [
    (0, "609-555-0124", "Karl"),
    (1, "609-555-1234", "Mike"),
    (3, "609-555-4302", "Ryan"),
]

@app.get("/customers/{id}")
def get_customer(id: int):
    # Find the customer by ID
    for customer in customers:
        if customer[0] == id:
            return {"id": customer[0], "phone": customer[1], "name": customer[2]}
    # Raise an HTTP exception if customer is not found
    raise HTTPException(status_code=404, detail="Customer not found")
