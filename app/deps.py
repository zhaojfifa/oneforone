from fastapi import Header, HTTPException
from .core.config import VALID_TOKENS

def require_token(x_access_token: str | None = Header(default=None)):
    if not x_access_token or x_access_token not in VALID_TOKENS:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_access_token   # (you could return user id if you map tokens)
