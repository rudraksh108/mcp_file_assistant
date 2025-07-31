# MCP File Assistant

An AI-powered file assistant to search, move, read, delete, and get metadata of your local files using simple language.

==========================
🚀 FEATURES
==========================
- Search files by name or keyword
- Move files across Desktop, Documents, Downloads (with renaming and subfolder support)
- Read preview of .txt and .pdf files
- Delete any indexed file with confirmation
- View metadata: size, creation date, last modified time
- Auto-refresh file indexing using watchdog

==========================
🏗️ PROJECT STRUCTURE
==========================
mcp/
├── cli/
│   └── assistant_client.py
├── servers/
│   └── src/filesystem/dist/index.js
├── tools/
│   ├── search.py
│   ├── move.py
│   ├── read.py
│   ├── delete.py
│   ├── metadata.py
│   ├── llm_client.py
│   └── command_router.py
├── file_index.json
├── indexer.py
├── requirements.txt
├── README.md
├── .env
└── main.py

==========================
⚙️ SETUP INSTRUCTIONS
==========================
1. Clone the repository:

   git clone git@github.com:rudraksh108/mcp_file_assistant.git
   cd mcp-file-assistant

2. Install dependencies:

   pip install -r requirements.txt

3. Create .env file and add:

   OPENROUTER_API_KEY=your_openrouter_key

4. Run the assistant:

   PYTHONPATH=. python cli/assistant_client.py

==========================
💬 EXAMPLE PROMPTS
==========================
- find cover letter
- move cover_letter.pdf to Documents/jobapps and rename it as application_letter
- read resume.txt
- delete notes.txt
- get metadata of file called report.pdf

==========================
🧠 LLM USAGE
==========================
- Model: mistralai/mistral-7b-instruct via OpenRouter
- Requires internet access for LLM
- All file operations run locally

==========================
📦 BUILD WINDOWS EXE
==========================
pip install pyinstaller
pyinstaller --onefile cli/assistant_client.py

Generated .exe will be in /dist folder.

==========================
👨‍💻 DEVELOPER
==========================
Shubham Gupta  
AI + File System Developer

==========================
📄 LICENSE
==========================
MIT License# mcp_file_assistant
