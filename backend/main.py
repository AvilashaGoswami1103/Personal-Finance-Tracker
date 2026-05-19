from fastapi import FastAPI    # Imports the FastAPI class from the FastAPI library
from pydantic import BaseModel    # pydantic used for data validation, data parsing, type checking
# suppose user sends amount = "hello", pydantic ensures that the amount must be float
from typing import List    # imports python type hints used for List[str]
from backend.services.analytics import calculate_analytics    # Imports your custom function from analytics.py
from backend.services.categorization import categorize_transaction
from backend.services.prediction import predict_spending

from backend.database.db import engine
from backend.database.db import Base
from backend.database.db import SessionLocal

from backend.models.transaction_model import TransactionDB
app = FastAPI()    # Creates your API application object.
Base.metadata.create_all(bind=engine)

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

    db = SessionLocal()     # opens a session connected to our SQLite database

    new_transaction = TransactionDB(    # Creates a new row (TransactionDB is your ORM model mapped to a table)
        amount=transaction.amount,
        description=transaction.description,
        category=predicted_category
    )

    db.add(new_transaction)     # stage the new row

    db.commit()     # write it permanently to database

    db.refresh(new_transaction)     # reload the object with its database-assigned values (like id).

    db.close()  # cleanly close the session

    return {
        "message": "Transaction added successfully",
        "predicted_category": predicted_category
    }

# Route 2: Get all transactions
@app.get("/transactions")
def get_transactions():

    db = SessionLocal()     # open a session connected to SQLite database

    transactions = db.query(TransactionDB).all()
    # queries all rows from the transactions table 

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
    # Pulls all transactions from the DB.
    # Passes them into your custom calculate_analytics function for summaries.

    db.close()

    return analytics

@app.get("/prediction")
def get_prediction():

    db = SessionLocal()

    transactions = db.query(TransactionDB).all()

    prediction = predict_spending([
        {
            "amount": t.amount,
            "category": t.category,
            "description": t.description
        }
        for t in transactions
    ])

    db.close()

    return prediction
