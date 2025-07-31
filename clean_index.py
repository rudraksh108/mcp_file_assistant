import json

with open("file_index.json", "r") as f:
    index = json.load(f)

cleaned = {}
for path, meta in index.items():
    if not any(skip in path.lower() for skip in ["pycharm", "venv", "node_modules", ".cache"]):
        cleaned[path] = meta

with open("file_index.json", "w") as f:
    json.dump(cleaned, f, indent=4)

print(f"✅ Cleaned index. Kept {len(cleaned)} entries.")
