# tools/delete.py

import os
import json

def delete_file(prompt: str) -> str:
    try:
        # ✅ Safe index file location
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
            return "❌ Koi matching file nahi mila index mein."

        # 🧠 Always prompt even if one match
        print("⚠️ Matching files:")
        for i, (path, name) in enumerate(candidates, 1):
            print(f"{i}. {name} → {path}")
        choice = input("👉 Enter file number to delete: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(candidates)):
            return "❌ Invalid selection."
        path, name = candidates[int(choice) - 1]

        # 🗑️ Delete the file
        os.remove(path)
        del index[path]

        # 📝 Update index
        with open(index_path, "w") as f:
            json.dump(index, f, indent=2)

        return f"🗑️ Deleted file: {name}"

    except Exception as e:
        return f"❌ Error while deleting file: {str(e)}"