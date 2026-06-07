from fastapi import FastAPI, Header, Depends, HTTPException    # Imports the FastAPI class from the FastAPI library
from pydantic import BaseModel    # pydantic used for data validation, data parsing, type checking
# suppose user sends amount = "hello", pydantic ensures that the amount must be float
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import List    # imports python type hints used for List[str]
from backend.services.analytics import calculate_analytics    # Imports your custom function from analytics.py
from backend.services.categorization import categorize_transaction
from backend.services.prediction import predict_future_spending

from backend.database.db import engine
from backend.database.db import Base
from backend.database.db import SessionLocal

from backend.models.transaction_model import TransactionDB
from backend.models.user_model import UserDB
from backend.utils.security import hash_password
from backend.utils.security import verify_password
from backend.utils.security import create_access_token
from backend.utils.security import verify_token
app = FastAPI()    # Creates your API application object.
Base.metadata.create_all(bind=engine)

# Temporary in-memory storage
transactions_db = []    # A Python list acting as a fake database

# Data model    Defines the structure of incoming data: a request schema
class Transaction(BaseModel):
    amount: float
    description: str
class User(BaseModel):
    username: str
    password: str
class LoginRequest(BaseModel):
    username: str
    password: str

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

    transaction_data = [

        {
            "amount": t.amount,
            "description": t.description,
            "category": t.category
        }

        for t in transactions
    ]

    db.close()

    return predict_future_spending(transaction_data)

@app.post("/register")
def register_user(user: User):

    db = SessionLocal()

    existing_user = db.query(UserDB).filter(
        UserDB.username == user.username
    ).first()

    if existing_user:

        db.close()

        return {
            "message":
            "Username already exists"
        }

    hashed_password = hash_password(
        user.password
    )

    new_user = UserDB(

        username=user.username,

        password_hash=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    db.close()

    return {
        "message":
        "User registered successfully"
    }

@app.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends()  # ← reads form fields
):
    db = SessionLocal()

    user = db.query(UserDB).filter(
        UserDB.username == form_data.username  # ← form_data.username
    ).first()

    if not user:
        db.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    valid_password = verify_password(
        form_data.password,        # ← form_data.password
        user.password_hash
    )

    if not valid_password:
        db.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    db.close()

    access_token = create_access_token({"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

@app.get("/profile")
def get_profile(
    token: str = Depends(oauth2_scheme)
):

    username = verify_token(token)

    if username is None:

        return {
            "message": "Invalid token"
        }

    return {
        "username": username
    }