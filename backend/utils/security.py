from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# passlib: A Python library for secure password hashing.
# CryptContext: A class that manages password encryption/decryption operations.

pwd_context = CryptContext( # creates password hashing context object
    schemes=["bcrypt"], # specifies the hashing algorithm to use
    # bcrypt: crytographic algorithm specifically designed for password hashing
    deprecated="auto"
    # Automatically handles legacy password hashes if you change algorithms later.
    # Allows gradual migration from old to new hashing methods.
)

SECRET_KEY = "finance_tracker_secret_key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password):    # function that takes a plain-text password as input

    return pwd_context.hash(password)
    # hashes the password using bcrypt:
    # Takes plain text (e.g., "MyPassword123")
    # Returns encrypted hash (e.g., "$2b$12$...")
    # One-way encryption: Cannot reverse the hash to get original password.
    # Each time you hash the same password, you get a different hash (due to random salt).

def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def create_access_token(data):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {"exp": expire}
    )

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_token(token):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        return username

    except JWTError:

        return None