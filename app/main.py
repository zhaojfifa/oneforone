from fastapi import FastAPI
from .routers import chat

app = FastAPI(title="My AI Service")
app.include_router(chat.router)

@app.get("/health")
def health():
    return {"status": "ok"}
