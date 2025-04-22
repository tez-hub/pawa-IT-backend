
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

venv\Scripts\activate  # On windows
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

POST /login

Logs in an existing user and returns a JWT token.

### Form fields

-   email: Email
-   password: Password

### Response

```bash
{
  "access_token": "<JWT Token>",
  "token_type": "bearer"
}

```

### Ask a Travel question

POST /ask

Sends a travel related question to the gemini model and gets a response.

### Headers

-   Authorization: Bearer <token>

### Body

```bash
{
  "question": "What are the best places to visit in Tokyo?"
}

```

### Response

```bash
{
  "response": "Here are some top attractions in Tokyo..."
}
```

The request and response are also saved in the database for future access.

## Get Query history

GET /history

Returns all past questions and Gemini responses for the authenticated user.

### Headers

-   Authorization: Bearer <token>

### Response

```bash
[
  {
    "question": "What are the best places to visit in Tokyo?",
    "response": "Here are some top attractions in Tokyo..."
  },
  ...
]

```


## Database Models

### User

-   user_id - Integer - Unique Id (primary Key)
-   email - String - Uniques user email
-   hashed_password - String - Password (hashed)


### UserRequest

-   id  -    Integer	    -   Request ID (Primary key)
-   user_id	-   String	-   ID of the user who made the request
-   question    -	String	-   The question asked
-   response	-   Text	-   The Gemini response
-   timestamp	-   DateTime	-   When the request was made


## Security
-   Passwords are hashed using bcrypt.
-   JWT tokens expire in 60 minutes.
-   All sensitive routes are protected using bearer token validation.


## CORS
CORS is enabled for local frontend development:

-   http://localhost:3000

-   http://127.0.0.1:3000


## Gemini Model
-   The app uses gemini-2.0-flash from Google’s Generative AI API.
-   Make sure to provide a valid GEMINI_API_KEY in the .env file.