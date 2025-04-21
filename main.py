from fastapi import FastAPI


app = FastAPI(title="AI Assistant Backend")

@app.get('/')
def root():
    return {"Hello": "World"}