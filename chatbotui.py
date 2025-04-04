import tkinter as tk
from tkinter import scrolledtext
import random

from education_chatbot.inference_engine import Chatbot
from education_chatbot.knowledge_base import KnowledgeBase
from education_chatbot.nlp_processor import NLPProcessor


# Assuming KnowledgeBase and NLPProcessor classes are already defined as above

class ChatbotUI:
    def __init__(self, master, chatbot):
        self.master = master
        self.master.title("Chatbot UI")

        # Initialize the chatbot
        self.chatbot = chatbot

        # Create the UI components
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=15, font=("Arial", 12))
        self.chat_area.grid(row=0, column=0, padx=10, pady=10)
        self.chat_area.config(state=tk.DISABLED)

        self.entry_box = tk.Entry(master, width=50, font=("Times New Roman", 12))
        self.entry_box.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = tk.Button(master, text="Send", command=self.send_message, font=("Arial", 12),
                                     background="pink")
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Bind the Enter key to trigger the send_message function
        self.entry_box.bind("<Return>", self.on_enter_pressed)

        # Create tag for bold text
        self.chat_area.tag_configure("bold", font=("Arial", 12, "bold"))

    def send_message(self):
        user_input = self.entry_box.get()
        if user_input:
            self.display_message(user_input, "User", "right")
            self.entry_box.delete(0, tk.END)
            response = self.chatbot.process_query(user_input)
            self.display_message(response, "Bot", "left")

    def on_enter_pressed(self, event):
        self.send_message()

    def display_message(self, message, sender, alignment):
        self.chat_area.config(state=tk.NORMAL)

        if alignment == "right":
            # Right-align the user message and bold the "User:"
            self.chat_area.insert(tk.END, f"{sender}: ", "bold")  # Bold the sender label
            self.chat_area.insert(tk.END, f"{message}\n\n")  # Add space after the user message
            self.chat_area.tag_add("right", "1.0", tk.END)
            self.chat_area.tag_configure("right", justify=tk.RIGHT)
        elif alignment == "left":
            # Left-align the bot message and bold the "Bot:"
            self.chat_area.insert(tk.END, f"{sender}: ", "bold")  # Bold the sender label
            self.chat_area.insert(tk.END, f"{message}\n\n")  # Add space after the bot message
            self.chat_area.tag_add("left", "1.0", tk.END)
            self.chat_area.tag_configure("left", justify=tk.LEFT)

        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)


# Sample database manager (to simulate dynamic data fetching from DB)
class DatabaseManager:
    def query_db(self, query):
        # Simulating database fetch (replace with actual DB query logic)
        return "This is a response from the database based on your query."


# Initialize the components
db_manager = DatabaseManager()
knowledge_base = KnowledgeBase(db_manager)
nlp_processor = NLPProcessor(db_manager)
chatbot = Chatbot(knowledge_base, nlp_processor)

# Create the Tkinter window and start the chatbot UI
root = tk.Tk()
chatbot_ui = ChatbotUI(root, chatbot)
root.mainloop()
