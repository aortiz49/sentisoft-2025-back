import os
from dotenv import load_dotenv

load_dotenv()

def get_claude_api_key():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Missing ANTHROPIC_API_KEY in environment variables.")
    return api_key
