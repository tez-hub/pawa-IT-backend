from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai
import os


app = FastAPI(title="AI Assistant Backend")

# The Frontend Origin
origins = ["http://localhost:3000"]

# Middlewares

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {"Hello": "World"}