# cli/assistant_client.py

import os
import sys
from tools.llm_client import call_llm
from tools.command_router import handle_prompt

def main():
    print("\n🤖 File Assistant Ready with LLM")
    print("📎 Examples:")
    print("   ➤ Move my test_resume to Desktop")
    print("   ➤ Find all PDFs from Documents")
    print("   ➤ Delete old_resume.txt from Downloads")
    print("   ➤ Read notes.txt from Desktop\n")

    try:
        while True:
            prompt = input("📝 Enter your prompt (or type 'exit'): ").strip()
            if not prompt:
                continue
            if prompt.lower() in {"exit", "quit"}:
                print("👋 Exiting assistant...")
                break

            # 🔍 Step 1: Use LLM to convert to file-style command
            try:
                llm_response = call_llm({
                    "messages": [{"role": "user", "content": prompt}]
                })
                interpreted_command = llm_response["choices"][0]["message"]["content"].strip()
                print(f"\n🤖 Interpreted Command: {interpreted_command}")
            except Exception as e:
                print(f"❌ LLM Error: {e}")
                continue

            # 🗂️ Step 2: Route command to appropriate handler
            try:
                fs_response = handle_prompt(interpreted_command)
                print(f"📁 Filesystem Result: {fs_response}\n")
            except Exception as e:
                print(f"❌ Filesystem Error: {e}")

    except KeyboardInterrupt:
        print("\n👋 Interrupted. Goodbye.")

if __name__ == "__main__":
    sys.path.insert(0, os.getcwd())  # 🛠️ Ensure root path is on sys.path
    main()