from sqlalchemy import create_engine
# creates an engine object, translates your Python commands into SQL statements that the database understands.
from sqlalchemy.ext.declarative import declarative_base
# Provides a base class for defining ORM models
# It sets up a mapping system so you can define tables as Python classes with attributes representing columns.
from sqlalchemy.orm import sessionmaker
# creates a fatory for database sessions. 
# A Session is your workspace for interacting with the database — you use it to query, add, update, and delete objects.

# SQLite database URL
DATABASE_URL = "sqlite:///./finance_tracker.db"
# Creates finance_tracker.db SQLite file in project directory.
# Here, sqlite:///./finance_tracker.db means:
# sqlite → use SQLite as the database dialect.
# /// → relative path (three slashes means local file).
# ./finance_tracker.db → create or connect to a file named finance_tracker.db in the current project directory.

# Create database engine: connection to database: Python <-> SQLite bridge
engine = create_engine( # builds the engine object
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    #SQLite-specific option: Setting check_same_thread=False allows the same connection to be safely used across multiple threads 
)

# Create session
# Database interaction object: used to insert data, read data, delete data
SessionLocal = sessionmaker(    # sessionmaker is a factory that generates session objects
    autocommit=False,
    # Means changes are not automatically saved to the database.
    # You must explicitly call session.commit() to persist changes.
    autoflush=False,
    # Normally, SQLAlchemy will “flush” (send pending changes to the database) before running a query.
    # Setting this to False means you control when flushing happens (usually when you commit).
    bind=engine
    # Tells the session which database engine to use (the one you created earlier with create_engine).
)

# now each time we do db=SessionLocal(), we get a fresh session object connected to our database

# Base class for models
Base = declarative_base()
# Creates a base class that your ORM models will inherit from.

# SessionLocal → lets you open sessions to interact with the database.
# Base → the foundation for defining your tables as Python classes.