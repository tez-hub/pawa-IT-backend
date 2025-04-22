
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import os
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# --- Local module imports ---
from auth import hash_password, verify_password, create_access_token, decode_access_token
from database import User, init_db, SessionLocal, UserRequest

# --- Environment & Gemini Configuration ---

# Load environment variables from a .env file
load_dotenv()

# Configure Gemini API key from env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# --- FastAPI App Setup ---

app = FastAPI()

# Set CORS origins (for frontend to interact with backend)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Add CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB (create tables if they don't exist)
init_db()

# --- OAuth2 Setup ---

# This dependency checks for a valid bearer token in the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic Schema ---

# Schema for the /ask route body
class TravelQuery(BaseModel):
    question: str

# --- Auth Routes ---

# Register a new user
@app.post("/register")
def register(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == form.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create and store new user with hashed password
    user = User(
        email=form.username,
        hashed_password=hash_password(form.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}

# Log in user and issue access token
@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Fetch user by email
    user = db.query(User).filter(User.email == form.username).first()

    # Check credentials
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create access token with user ID
    token = create_access_token({"user_id": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}

# --- Gemini Query Route ---

# Authenticated route to ask questions to Gemini
@app.post("/ask")
async def ask(
    query: TravelQuery,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    # Decode the token to get user ID
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        # Send question to Gemini and get response
        response = model.generate_content(query.question)
        answer = response.text

        # Save request and response to the database
        db_request = UserRequest(
            user_id=user_id,
            question=query.question,
            response=answer
        )
        db.add(db_request)
        db.commit()
        db.refresh(db_request)

        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini Error: {str(e)}")

# --- User Query History ---

# Get past queries made by authenticated user
@app.get("/history")
def get_history(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # Decode user ID from token
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Fetch all past questions/answers for this user
    records = db.query(UserRequest).filter(UserRequest.user_id == user_id).order_by(UserRequest.id.desc()).all()

    # Return them as a list of dictionaries
    return [
        {"question": r.question, "response": r.response}
        for r in records
    ]
