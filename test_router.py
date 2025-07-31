# test_router.py

from tools.command_router import handle_prompt

while True:
    user_input = input("🧠 Your command (or 'exit'): ")
    if user_input.lower() == "exit":
        break

    response = handle_prompt(user_input)
    print(response)
