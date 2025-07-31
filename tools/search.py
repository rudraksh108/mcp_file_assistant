# tools/search.py

import json
import os
from datetime import datetime

def search_files(input_text: str) -> str:
    try:
        index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "file_index.json"))
        if not os.path.exists(index_path):
            return "❌ file_index.json not found."

        with open(index_path, "r") as f:
            index = json.load(f)

        query = input_text.lower().strip()
        query_tokens = set(query.replace("_", " ").replace("-", " ").split())

        matches = []

        for path, meta in index.items():
            if not os.path.exists(path):
                continue  # Skip deleted/moved files

            filename = meta["original_name"].lower()
            name_tokens = set(filename.replace("_", " ").replace("-", " ").split())

            # ✅ Match if any query word is in filename tokens or full query is in filename
            if query in filename or query_tokens & name_tokens:
                modified_time = os.path.getmtime(path)
                matches.append({
                    "filename": meta["original_name"],
                    "path": path,
                    "modified": modified_time
                })

        if not matches:
            return f"❌ No matching files found for: '{input_text}'"

        # Sort by modified time
        matches.sort(key=lambda x: x["modified"], reverse=True)

        lines = ["📁 Matching Files (sorted by last modified):\n"]
        for match in matches:
            mod_time_str = datetime.fromtimestamp(match["modified"]).strftime("%Y-%m-%d %H:%M:%S")
            lines.append(
                f"📄 {match['filename']}\n📍 Path: {match['path']}\n🕒 Last Modified: {mod_time_str}\n"
            )

        lines.append(f"✅ Latest file: {matches[0]['filename']}")
        return "\n".join(lines)

    except Exception as e:
        return f"❌ Error searching files: {str(e)}"