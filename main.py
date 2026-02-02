from ai_researcher.agent import chat


def main():
    print("🤖 AI Research Agent (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye 👋")
            break

        response = chat(user_input)
        print(f"AI: {response}\n")


if __name__ == "__main__":
    main()
