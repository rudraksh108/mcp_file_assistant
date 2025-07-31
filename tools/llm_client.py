# tools/llm_client.py

from openai import OpenAI
from dotenv import load_dotenv
import os

# ✅ Load API key from .env
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL")
model = "mistralai/mistral-7b-instruct"

if not api_key or not base_url:
    raise EnvironmentError("❌ API key or Base URL missing. Check your .env file.")

# ✅ Initialize OpenAI-compatible client
client = OpenAI(api_key=api_key, base_url=base_url)


def call_llm(request: dict) -> dict:
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
