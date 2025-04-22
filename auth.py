# Importing the CryptContext class from passlib for password hashing
from passlib.context import CryptContext 

# Importing JWTError for handling exceptions, and jwt for encoding/decoding JSON Web Tokens
from jose import JWTError, jwt

# Importing datetime classes for handling token expiration
from datetime import datetime, timedelta

# Constants for JWT token encoding
SECRET_KEY = "your-secret-key"  # Secret key used to sign the JWT
ALGORITHM = "HS256"             # Hashing algorithm to use for signing the token
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token expiration time in minutes

# Initializing the password context with bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a plain password
def hash_password(password: str):
    # Uses the bcrypt algorithm to hash the password securely
    return pwd_context.hash(password)

# Function to verify a password
def verify_password(plain_password, hashed_password):
    # Compares a plain password with its hashed version
    return pwd_context.verify(plain_password, hashed_password)

# Function to create a JWT access token
def create_access_token(data: dict):
    # Create a copy of the data to avoid modifying the original dictionary
    to_encode = data.copy()

    # Set the expiration time for the token
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add the expiration time to the data being encoded
    to_encode.update({"exp": expire})

    # Create and return the encoded JWT token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to decode and validate a JWT token
def decode_access_token(token: str):
    try:
        # Decode the JWT token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract and return the user_id from the payload
        return payload.get("user_id")
    except JWTError:
        # If decoding fails (e.g., invalid token or expired), return None
        return None
