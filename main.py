from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
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

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

@app.post('/api/travel-agent')
async def get_travel_agent(request: Request):
    data = await request.json()
    user_query = data.get("query")

    prompt = f"""You're a travel documentation assistant. Help with:
    "{user_query}". 
    Return visa requirements, passport info, advisories, and links."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"answer": response.choices[0].message["content"]}