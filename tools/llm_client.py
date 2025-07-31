# cli/llm_client.py

from openai import OpenAI
from dotenv import load_dotenv
import os

# ✅ Load API key from .env
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# ✅ Configurable parameters
base_url = "https://openrouter.ai/api/v1"
model = "mistralai/mistral-7b-instruct"

# ✅ Initialize OpenAI-compatible client
client = OpenAI(api_key=api_key, base_url=base_url)

def call_llm(request: dict) -> dict:
    """
    Takes a chat-style prompt request and returns the LLM response in dictionary format.
    Enforces a system prompt that tells the LLM to reply with file assistant-style instructions only.
    """
    user_messages = request.get("messages", [])
    if not user_messages:
        raise ValueError("Missing 'messages' in request")

    system_prompt = {
        "role": "system",
        "content": (
            "You are a file assistant. Your task is to convert the user's natural language request "
            "into a clean, simple command like:\n"
            "- 'move test.txt to Desktop'\n"
            "- 'read resume.pdf from Downloads'\n"
            "- 'delete notes.txt from Documents'\n"
            "Do NOT explain or respond with anything else."
        )
    }

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[system_prompt] + user_messages,
            temperature=0.0
        )
        return response.model_dump()
    except Exception as e:
        raise RuntimeError(f"❌ LLM error: {e}")