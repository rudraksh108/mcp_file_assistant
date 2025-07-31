import os
import json
import datetime
import stat

# ✅ Safe path to file_index.json
INDEX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "file_index.json"))

def get_file_metadata(prompt: str) -> str:
    try:
        if not os.path.exists(INDEX_PATH):
            return f"❌ file_index.json not found at: {INDEX_PATH}"

        with open(INDEX_PATH, "r") as f:
            index = json.load(f)

        prompt_lower = prompt.lower()
        prompt_tokens = set(prompt_lower.replace("_", " ").replace("-", " ").split())

        for path, meta in index.items():
            if not os.path.exists(path):
                continue
            file_name = meta.get("original_name", "").lower()
            name_tokens = set(file_name.replace("_", " ").replace("-", " ").split())

            # Match full filename or any token
            if file_name in prompt_lower or prompt_tokens & name_tokens:
                stats = os.stat(path)
                size_kb = stats.st_size / 1024
                created = datetime.datetime.fromtimestamp(stats.st_ctime)
                modified = datetime.datetime.fromtimestamp(stats.st_mtime)
                file_type = os.path.splitext(path)[1] or "No extension"
                permissions = stat.filemode(stats.st_mode)

                return f"""📄 Metadata for '{meta['original_name']}':
• 📍 Full Path: {path}
• 📦 File Size: {size_kb:.2f} KB
• 🗓️ Created On: {created.strftime('%Y-%m-%d %H:%M:%S')}
• ✏️ Last Modified: {modified.strftime('%Y-%m-%d %H:%M:%S')}
• 🧾 File Type: {file_type}
• 🔐 Permissions: {permissions}"""

        return "❌ File not found in index."

    except Exception as e:
        return f"❌ Error getting metadata: {str(e)}"