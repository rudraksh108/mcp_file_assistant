# tools/move.py

import os
import json
import shutil
import re

def move_file(prompt: str) -> str:
    try:
        index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "file_index.json"))
        if not os.path.exists(index_path):
            return f"❌ file_index.json not found at: {index_path}"

        with open(index_path, "r") as f:
            index = json.load(f)

        prompt_lower = prompt.lower()
        words = prompt_lower.split()
        matching_files = []

        skip_folders = ["pycharm", ".venv", "venv", ".cache", "node_modules", "__pycache__"]

        # 🔍 Match by file name
        for path, meta in index.items():
            if any(skip in path.lower() for skip in skip_folders):
                continue
            name = meta["original_name"].lower()
            if any(word in name and len(word) > 3 for word in words):
                matching_files.append((path, meta["original_name"]))

        if not matching_files:
            return "❌ Koi matching file nahi mili index mein."

        if len(matching_files) > 10:
            return f"⚠️ Bahut saari matches mil gayi ({len(matching_files)}). Prompt thoda aur specific likho."

        # 🙋‍♂️ Always ask if multiple matches
        if len(matching_files) > 1:
            print("⚠️ Multiple files mil gayi. Select one:")
            for i, (path, name) in enumerate(matching_files, 1):
                print(f"{i}. {name} → {path}")
            choice = input("👉 Enter file number to proceed: ").strip()
            if not choice.isdigit() or not (1 <= int(choice) <= len(matching_files)):
                return "❌ Invalid selection."
            src_path, original_name = matching_files[int(choice) - 1]
        else:
            src_path, original_name = matching_files[0]

        # 📂 Destination folder detection
        folder_map = {
            "desktop": os.path.expanduser("~/Desktop"),
            "documents": os.path.expanduser("~/Documents"),
            "downloads": os.path.expanduser("~/Downloads")
        }

        # 🧠 Full path like "documents/jobapps"
        dest_path_match = re.search(r"(desktop|documents|downloads)[/\\]([\w\-_ /]+)", prompt_lower)
        if dest_path_match:
            base = dest_path_match.group(1)
            subfolder = dest_path_match.group(2).strip().replace(" ", "_")
            dest_dir = os.path.join(folder_map[base], subfolder)
        else:
            # fallback: just documents, then optional folder "called xyz"
            base = next((b for b in folder_map if b in prompt_lower), None)
            if not base:
                return "❌ Destination folder nahi mila (mention 'desktop', 'documents', ya 'downloads')."
            dest_dir = folder_map[base]

            folder_match = re.search(r"folder (?:called|named)\s+(?:\"|')?([a-zA-Z0-9_\- ]+)(?:\"|')?", prompt_lower)
            if folder_match:
                folder_name = folder_match.group(1).strip().replace(" ", "_")
                dest_dir = os.path.join(dest_dir, folder_name)

        os.makedirs(dest_dir, exist_ok=True)

        # ✏️ Rename if asked
        new_name = original_name
        rename_phrases = ["rename it as", "call it", "name it as", "name it"]
        for phrase in rename_phrases:
            if phrase in prompt_lower:
                try:
                    parts = prompt_lower.split(phrase)[1].strip().split()
                    new_base = parts[0].replace('"', '').replace("'", "")
                    new_name = new_base + os.path.splitext(original_name)[1]
                    break
                except:
                    return "❌ Rename ka naam samajh nahi aaya."

        dest_path = os.path.join(dest_dir, new_name)

        # 🚚 Move operation
        try:
            shutil.move(src_path, dest_path)
        except Exception as e:
            return f"❌ Move failed: {e}"

        # 📝 Update index
        del index[src_path]
        index[dest_path] = {"original_name": new_name}
        with open(index_path, "w") as f:
            json.dump(index, f, indent=2)

        return f"✅ File '{original_name}' moved to '{dest_path}' as '{new_name}'"

    except Exception as e:
        return f"❌ Error: {str(e)}"