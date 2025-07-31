from openai import OpenAI

# ✅ Hardcoded API key and base URL
api_key = "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"
base_url = "https://openrouter.ai/api/v1"
model = "mistralai/mistral-7b-instruct"

# ✅ Initialize client
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
        )
        return response.model_dump()
    except Exception as e:
        raise RuntimeError(f"❌ LLM error: {e}")
