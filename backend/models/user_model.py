# CREATE TABLE users (
#     id INTEGER PRIMARY KEY,
#     username TEXT UNIQUE,
#     password_hash TEXT
# );

from sqlalchemy import Column, Integer, String
# ORM (Object-relational mapping): Maps Python classes to database tables automatically
# Column: Defines database columns
# Integer: Data type for integer values
# String: Data type for text values

from backend.database.db import Base
# Imports the SQLAlchemy Base class (declarative base for all models). This connects the model to the database configuration.
class UserDB(Base): 
# inheriting from Base automatically regusters this model with the database

    __tablename__ = "users" # specifies the actual table name in the database that this model corresponds to
    # SQLAlchemy uses this to create/reference the usrs table in the database
    # defining
    id = Column(
        Integer,    # SQLAlchemy automatically auto-increments this (1, 2, 3...).
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        index=True
    )

    password_hash = Column( # database column for storing encrypted passwords
        String
    )