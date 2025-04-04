class ChatbotUI:
    def __init__(self, chatbot):
        self.chatbot = chatbot

    def start_chat(self):
        print("Education Counseling Chatbot: Type 'exit' to end the conversation.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Chatbot: Goodbye!")
                break
            response = self.chatbot.process_query(user_input)
            print(f"Chatbot: {response}")
