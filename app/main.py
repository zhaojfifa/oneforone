# app/main.py
from fastapi import FastAPI, Query
from .routers import chat

app = FastAPI(title="My AI Service")
app.include_router(chat.router)

@app.get("/chat-test")
def chat_test(prompt: str = Query(..., min_length=1)):
    return {"answer": f"你输入了: {prompt}"}
