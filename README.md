
## Overview

This is a FastAPI-based backend application that allows users to:

-   Register and log in with secure authentication.

-   Ask travel-related questions using Google's Gemini AI model.

-   Retrieve their question-answer history.

The backend supports token-based authentication via JWT, and stores user information and queries in a SQLite database using SQLAlchemy ORM.

### Files in this project

```bash
main.py             # FastAPI app. I have included the routes here. It is not a large app anyway.
database.py         # SQLAlchemy DB setup and models
auth.py             # Authentication utils (password hashing, JWT)
.env                # Environment variables (e.g. GEMINI_API_KEY)
requirements.txt    # The libraries to be installed.
```


### Tech Stack

-    FastAPI - for building APIs.
-    SQLite - for data storage.
-    SQLAlchemy - for ORM.
-   Passlib (bcrypt) - for password hashing.
-   JWT (JOSE) - for secure token-based authentication.
-   Google Generative AI - for processing travel queries.
-   Pydantic - for request validation.



# Setuo Instructions
1. Clone the repo 

```bash
git clone https://github.com/tez-hub/pawa-IT-backend.git
cd the-name-you-have-named-the-folder

```

2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Mac or Linux
or 

venv\Scripts\activate
```

3. Install dependancies

```bash
pip install -r requirements.txt
```

4. Set up your .env file

Create a .env file and add your Gemini API Key:

```bash
GEMINI_API_KEY=gemini_api_key
```

5. Run the app.

```bash
uvicorn main:app --reload
```

After that, your FastAPI should be running at: http://127.0.0.1:8000


# Authentication

Authentication is done using OAuth2 with Password Flow and JWT tokens.

Token Format

-   When a user logs in, a JWT token is issued.
-   This token must be included in requests to protected endpoints using the Authorization: Bearer <token> header.

# API Endpoints

## REGISTER

POST /register

-   It registers a new user.

### Form fields
-   username: Email (used as login)
-   password: Passwoed

### Response

```bash
{
  "message": "User registered successfully"
}
```


## Login


