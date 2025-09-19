# app/routers/chat.py
import os
from typing import Optional

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

import httpx
from openai import OpenAI

router = APIRouter(prefix="", tags=["chat"])

# ---------- 配置 ----------
ALLOWED_TOKENS = {
    "A": os.getenv("USER_TOKEN_A", ""),  # 仅开放用户A
    # 以后如果要允许B/C，填上就行：
    # "B": os.getenv("USER_TOKEN_B", ""),
    # "C": os.getenv("USER_TOKEN_C", ""),
}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # 不直接抛错，留到首次请求时报 500，方便 Render 启动
    pass

# 初始化 OpenAI 客户端（v1.x）
client = OpenAI(api_key=OPENAI_API_KEY)

# ---------- 请求/响应模型 ----------
class ChatIn(BaseModel):
    prompt: str = Field(..., description="用户提问/输入")
    model: str = Field(default="gpt-4o-mini", description="OpenAI 模型名")
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=None, ge=1)


class ChatOut(BaseModel):
    answer: str
    model: str
    usage: Optional[dict] = None


# ---------- 鉴权 ----------
def verify_token(x_access_token: Optional[str]) -> None:
    if not x_access_token:
        raise HTTPException(status_code=401, detail="Missing X-Access-Token")
    # 仅允许用户A
    if x_access_token != ALLOWED_TOKENS.get("A"):
        raise HTTPException(status_code=403, detail="Forbidden")


# ---------- 同步接口 ----------
@router.post("/chat", response_model=ChatOut)
async def chat(
    body: ChatIn,
    x_access_token: Optional[str] = Header(None),
):
    verify_token(x_access_token)

    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")

    try:
        # 调 OpenAI Chat Completions
        resp = client.chat.completions.create(
            model=body.model,
            messages=[{"role": "user", "content": body.prompt}],
            temperature=body.temperature,
            max_tokens=body.max_tokens,
        )
        msg = resp.choices[0].message.content or ""
        usage = {
            "prompt_tokens": getattr(resp.usage, "prompt_tokens", None),
            "completion_tokens": getattr(resp.usage, "completion_tokens", None),
            "total_tokens": getattr(resp.usage, "total_tokens", None),
        }
        return ChatOut(answer=msg, model=body.model, usage=usage)
    except httpx.HTTPError as e:
        # 网络层异常
        raise HTTPException(status_code=502, detail=f"Upstream error: {e}")
    except Exception as e:
        # 其它异常
        raise HTTPException(status_code=500, detail=f"Server error: {e}")


# ---------- 可选：SSE流式接口 ----------
from fastapi import Request
from fastapi.responses import StreamingResponse

@router.post("/chat/stream")
async def chat_stream(
    request: Request,
    body: ChatIn,
    x_access_token: Optional[str] = Header(None),
):
    verify_token(x_access_token)
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")

    def event_generator():
        try:
            stream = client.chat.completions.create(
                model=body.model,
                messages=[{"role": "user", "content": body.prompt}],
                temperature=body.temperature,
                max_tokens=body.max_tokens,
                stream=True,         # 开启流式
            )
            for chunk in stream:
                if hasattr(chunk.choices[0].delta, "content"):
                    token = chunk.choices[0].delta.content or ""
                    if token:
                        yield f"data: {token}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: [ERROR] {e}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
