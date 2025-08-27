from fastapi import FastAPI

app = FastAPI(title="My AI Service (minimal)")

@app.get("/health")
def health():
    return {"ok": True}
