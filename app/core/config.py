import os

# service name (optional)
SERVICE_NAME = os.getenv("SERVICE_NAME", "My AI Service")

# 3 user tokens (set as env vars locally / on Render)
VALID_TOKENS = {
    os.getenv("USER_TOKEN_A", ""),
    os.getenv("USER_TOKEN_B", ""),
    os.getenv("USER_TOKEN_C", ""),
}

# if you’ll call a real AI provider, keep its key here
AI_API_KEY = os.getenv("AI_API_KEY", "")
