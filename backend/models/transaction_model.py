from sqlalchemy import Column, Integer, Float, String
from backend.database.db import Base

class TransactionDB(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Float)

    description = Column(String)

    category = Column(String)