# indexer.py

import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

INDEX_PATH = "file_index.json"
WATCH_DIRS = [
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Desktop")
]
SKIP_FOLDERS = [".venv", "venv", "node_modules", "__pycache__", ".cache", "pycharm"]

def is_valid_file(path):
    return os.path.isfile(path) and not any(skip in path for skip in SKIP_FOLDERS)

def build_index():
    index = {}
    for base_dir in WATCH_DIRS:
        for root, _, files in os.walk(base_dir):
            if any(skip in root for skip in SKIP_FOLDERS):
                continue
            for f in files:
                full_path = os.path.join(root, f)
                if is_valid_file(full_path):
                    index[full_path] = {"original_name": f}
    with open(INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)
    print(f"✅ Rebuilt full index with {len(index)} files.")
    return index

def update_index(path, index):
    if is_valid_file(path):
        index[path] = {"original_name": os.path.basename(path)}
    elif path in index:
        del index[path]
    with open(INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)
    print(f"🛠️ Index updated for: {path}")

class IndexUpdater(FileSystemEventHandler):
    def __init__(self, index):
        self.index = index

    def on_created(self, event):
        update_index(event.src_path, self.index)

    def on_deleted(self, event):
        update_index(event.src_path, self.index)

    def on_moved(self, event):
        update_index(event.src_path, self.index)
        update_index(event.dest_path, self.index)

    def on_modified(self, event):
        update_index(event.src_path, self.index)

if __name__ == "__main__":
    index = build_index()
    event_handler = IndexUpdater(index)
    observer = Observer()
    for dir in WATCH_DIRS:
        observer.schedule(event_handler, dir, recursive=True)
    observer.start()
    print("📡 Auto-refresh file indexing started...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()