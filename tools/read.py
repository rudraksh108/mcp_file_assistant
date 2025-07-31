# tools/read.py

import json
import os
import fitz  # PyMuPDF

def read_file(prompt: str) -> str:
    try:
        # ✅ Use absolute path for index
        index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "file_index.json"))
        if not os.path.exists(index_path):
            return f"❌ file_index.json not found at: {index_path}"

        with open(index_path, "r") as f:
            index = json.load(f)

        prompt_lower = prompt.lower()
        candidates = []

        for path, meta in index.items():
            if not os.path.exists(path):
                continue
            filename = meta["original_name"].lower()
            if filename in prompt_lower or any(word in filename for word in prompt_lower.split()):
                candidates.append((path, meta["original_name"]))

        if not candidates:
            return "❌ File not found in index."

        # 🧠 Always prompt if multiple
        print("⚠️ Multiple matching files found. Choose one:" if len(candidates) > 1 else "")
        for i, (path, name) in enumerate(candidates, 1):
            print(f"{i}. {name} → {path}")
        choice = input("👉 Enter file number to read: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(candidates)):
            return "❌ Invalid selection."
        path, original_name = candidates[int(choice) - 1]

        # 📖 PDF logic
        if path.endswith(".pdf"):
            try:
                doc = fitz.open(path)
                text = ""
                for page in doc:
                    text += page.get_text()
                    if len(text) > 1000:
                        break
                doc.close()
                return f"📖 PDF Preview of '{original_name}':\n\n{text[:1000]}"
            except Exception as e:
                return f"❌ Error reading PDF: {str(e)}"

        # 📖 Text or others
        else:
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read(1000)
                return f"📖 First part of '{original_name}':\n\n{content}"

    except Exception as e:
        return f"❌ Error reading file: {str(e)}"