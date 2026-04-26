from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from backend.services.analytics import calculate_analytics

app = FastAPI()

# Temporary in-memory storage
transactions_db = []

# Data model
class Transaction(BaseModel):
    amount: float
    category: str
    description: str


# Route 1: Add transaction
@app.post("/add_transaction")
def add_transaction(transaction: Transaction):
    transactions_db.append(transaction.dict())  # ✅ convert to dict
    return {"message": "Transaction added successfully"}

# Route 2: Get all transactions
@app.get("/transactions")
def get_transactions():
    return transactions_db


# Route 3: Get analytics
@app.get("/analytics")
def get_analytics():
    return calculate_analytics(transactions_db)

