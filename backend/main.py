from fastapi import FastAPI    # Imports the FastAPI class from the FastAPI library
from pydantic import BaseModel    # pydantic used for data validation, data parsing, type checking
# suppose user sends amount = "hello", pydantic ensures that the amount must be float
from typing import List    # imports python type hints used for List[str]
from backend.services.analytics import calculate_analytics    # Imports your custom function from analytics.py
from backend.services.categorization import categorize_transaction

app = FastAPI()    # Creates your API application object.

# Temporary in-memory storage
transactions_db = []    # A Python list acting as a fake database

# Data model    Defines the structure of incoming data: a request schema
class Transaction(BaseModel):
    amount: float
    description: str

# REST API

# # Route 1: Add transaction
# @app.post("/add_transaction")    # API route - Create an API endpoint
# # POST is used to send data, create new reocrds
# # FastAPI registers: "/add_transaction"
# def add_transaction(transaction: Transaction):
#     transactions_db.append(transaction.dict())  # ✅ convert to dict
#     # Converts Pydantic object → Python dictionary
#     return {"message": "Transaction added successfully"}
#     # FastAPI automatically converts Python dict → JSON response and send back to browser

# @app.post("/add_transaction")
# def add_transaction(transaction: Transaction):

#     predicted_category = categorize_transaction(
#         transaction.description
#     )

#     transaction_data = {
#         "amount": transaction.amount,
#         "description": transaction.description,
#         "category": predicted_category
#     }

#     transactions_db.append(transaction_data)

#     return {
#         "message": "Transaction added successfully",
#         "predicted_category": predicted_category
#     }


@app.post("/add_transaction")
def add_transaction(transaction: Transaction):

    predicted_category = categorize_transaction(
        transaction.description
    )

    db = SessionLocal()

    new_transaction = TransactionDB(
        amount=transaction.amount,
        description=transaction.description,
        category=predicted_category
    )

    db.add(new_transaction)

    db.commit()

    db.refresh(new_transaction)

    db.close()

    return {
        "message": "Transaction added successfully",
        "predicted_category": predicted_category
    }

# Route 2: Get all transactions
@app.get("/transactions")
def get_transactions():

    db = SessionLocal()

    transactions = db.query(TransactionDB).all()

    db.close()

    return transactions


# Route 3: Get analytics
@app.get("/analytics")
def get_analytics():
    # return calculate_analytics(transactions_db)    #Passes all transactions into calculate_analytics()
    db = SessionLocal()

    transactions = db.query(TransactionDB).all()

    analytics = calculate_analytics([
        {
            "amount": t.amount,
            "category": t.category,
            "description": t.description
        }
        for t in transactions
    ])

    db.close()

    return analytics
