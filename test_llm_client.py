from tools.llm_client import call_llm

request = {
    "messages": [
        {"role": "user", "content": "Hello, what can you do?"}
    ]
}

try:
    response = call_llm(request)
    print("✅ LLM Response:")
    print(response["choices"][0]["message"]["content"])
except Exception as e:
    print(e)
