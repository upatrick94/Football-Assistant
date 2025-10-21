from tools.agent import football_agent

while True:
    user_input = input("\n⚽ Ask your Football Assistant: ")
    if user_input.lower() in ["quit", "exit"]:
        break
    response = football_agent(user_input)
    print("\n🤖", response)
