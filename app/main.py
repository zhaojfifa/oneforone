from fastapi import FastAPI
from .routers.chat import router as chat_router

app = FastAPI(title="My AI Service")

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(chat_router)

