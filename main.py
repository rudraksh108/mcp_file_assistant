import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain_community.chat_models import ChatOpenAI

# Import tools
from tools.read import read_file
from tools.move import move_file
from tools.delete import delete_file
from tools.search import search_files
from tools.metadata import get_file_metadata

# ------------------------
# 🔐 Load API Key
# ------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ------------------------
# 🛠️ Define Tools
# ------------------------
tools = [
    Tool(
        name="SearchFiles",
        func=search_files,
        description="Use this to search for files by keyword. Input should be a string keyword."
    ),
    Tool(
        name="DeleteFile",
        func=delete_file,
        description="Use this to delete a file. Input should contain the file name."
    ),
    Tool(
        name="ReadFile",
        func=read_file,
        description="Use this to read a file. Input should contain the file name."
    ),
    Tool(
        name="MoveFile",
        func=move_file,
        description="Use this to move a file. Input should contain the file name and destination path."
    ),
    Tool(
        name="GetFileMetadata",
        func=get_file_metadata,
        description="Use this to get metadata of a file. Input should contain the file name."
    )
]

# ------------------------
# 🤖 Setup LLM Agent
# ------------------------
llm = ChatOpenAI(
    openai_api_key=api_key,
    temperature=0,
    model_name="gpt-3.5-turbo"
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# ------------------------
# 🧪 Mock fallback if quota exceeds
# ------------------------
def mock_response(prompt):
    prompt = prompt.lower()

    if "search" in prompt:
        return search_files(prompt)
    elif "read" in prompt:
        return read_file(prompt)
    elif "delete" in prompt:
        return delete_file(prompt)
    elif "move" in prompt:
        return move_file(prompt)
    elif "metadata" in prompt or "details" in prompt:
        return get_file_metadata(prompt)
    else:
        return "🤖 Sorry, I can't perform that action in mock mode."

# ------------------------
# 🚀 Interactive CLI
# ------------------------
if __name__ == "__main__":
    print("🧠 Welcome to your File Assistant! (type 'exit' to quit)")
    while True:
        user_input = input("\n🗣️ What do you want to do?\n> ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting... Have a great day!")
            break
        try:
            response = agent.run(user_input)
            print("🤖:", response)
        except Exception as e:
            if "quota" in str(e).lower():
                print("⚠️ [Mock Mode] OpenAI quota exhausted. Showing simulated output:")
                print("🤖:", mock_response(user_input))
            else:
                print("❌ Error:", e)
