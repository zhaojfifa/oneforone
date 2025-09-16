from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

# 允许的3个 token（Render 上用环境变量注入，本地开发可先 export）
TOKENS = {os.getenv("USER_TOKEN_A"), os.getenv("USER_TOKEN_B"), os.getenv("USER_TOKEN_C")}

class ChatIn(BaseModel):
    prompt: str

@router.post("/chat")
def chat(payload: ChatIn, x_access_token: str = Header(None)):
    if not x_access_token or x_access_token not in TOKENS:
        raise HTTPException(status_code=401, detail="invalid token")
    # 先回显；后续你可接入真实大模型
    return {"answer": f"you said: {payload.prompt}"}
