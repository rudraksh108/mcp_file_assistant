# tools/command_router.py

import os
import subprocess

from tools.search import search_files
from tools.move import move_file
from tools.read import read_file
from tools.delete import delete_file
from tools.metadata import get_file_metadata  # optional, if you want metadata too

# ✅ Start MCP Filesystem Server only once when this module is imported
def start_mcp_filesystem_server():
    server_path = os.path.abspath("servers/src/filesystem/dist/index.js")
    allowed_dir = os.path.expanduser("~/Downloads")  # You can allow multiple directories if needed
    try:
        process = subprocess.Popen(
            ["node", server_path, allowed_dir],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✅ MCP Filesystem Server started.")
        return process
    except Exception as e:
        print(f"❌ Failed to start MCP server: {e}")
        return None

# 🛠️ Launch MCP server automatically on module load
mcp_server_process = start_mcp_filesystem_server()


# 🧠 Route the natural language command to the appropriate tool
def handle_prompt(prompt: str) -> str:
    prompt_lower = prompt.lower()

    if any(word in prompt_lower for word in ["move", "shift", "transfer"]):
        return move_file(prompt)

    elif any(word in prompt_lower for word in ["delete", "remove"]):
        return delete_file(prompt)

    elif any(word in prompt_lower for word in ["find", "search", "locate"]):
        return search_files(prompt)

    elif any(word in prompt_lower for word in ["read", "open", "show content", "show contents"]):
        return read_file(prompt)

    elif any(word in prompt_lower for word in ["metadata", "details", "info about", "properties"]):
        return get_file_metadata(prompt)

    else:
        return "🤖 Sorry, couldn't understand the command."