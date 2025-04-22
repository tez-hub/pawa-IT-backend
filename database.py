# Import necessary SQLAlchemy components for defining models and database sessions
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import datetime module to set default timestamp values
from datetime import datetime

# SQLite database URL (can be changed to PostgreSQL/MySQL URI if needed)
DATABASE_URL = "sqlite:///./travel_assistant.db"

# Create a base class for the ORM models using declarative system
Base = declarative_base()

# Create the database engine; connect_args is specific to SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class for database interaction
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM model representing user queries and assistant responses
class UserRequest(Base):
    __tablename__ = "user_requests"  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each request
    user_id = Column(String, index=True)  # ID of the user making the request
    question = Column(Text)  # The question asked by the user
    response = Column(Text)  # The assistant's response
    timestamp = Column(DateTime, default=datetime.utcnow)  # Timestamp of the request (default = now)

# ORM model representing registered users
class User(Base):
    __tablename__ = "users"  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each user
    email = Column(String, unique=True, index=True)  # User's email address (must be unique)
    hashed_password = Column(String)  # Hashed version of the user's password

# Function to create all tables in the database
def init_db():
    # This will create tables for all models that inherit from Base
    Base.metadata.create_all(bind=engine)
