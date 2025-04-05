import tkinter as tk
from tkinter import scrolledtext
import os


class ChatbotUI:
    def __init__(self, master, chatbot, nlp_processor, ml_model=None):
        self.master = master
        self.chatbot = chatbot
        self.nlp_processor = nlp_processor
        self.ml_model = ml_model
        self.awaiting_learning = False
        self.last_question = ""
        self.setup_ui()

    def setup_ui(self):
        """Initialize the user interface components"""
        self.master.title("Education Counseling Chatbot")

        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(
            self.master,
            wrap=tk.WORD,
            width=60,
            height=15,
            font=("Arial", 12),
            state=tk.DISABLED
        )
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # User input entry
        self.entry_box = tk.Entry(
            self.master,
            width=50,
            font=("Times New Roman", 12)
        )
        self.entry_box.grid(row=1, column=0, padx=10, pady=10)
        self.entry_box.bind("<Return>", self.on_enter_pressed)

        # Send button
        self.send_button = tk.Button(
            self.master,
            text="Send",
            command=self.send_message,
            font=("Arial", 12),
            background="#4CAF50",  # Green color
            foreground="white"
        )
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Configure text tags
        self.chat_area.tag_configure("user",
                                     font=("Arial", 12, "bold"),
                                     foreground="#333333")
        self.chat_area.tag_configure("bot",
                                     font=("Arial", 12),
                                     foreground="#0066CC")
        self.chat_area.tag_configure("right", justify=tk.RIGHT)
        self.chat_area.tag_configure("left", justify=tk.LEFT)

    def send_message(self, event=None):
        """Handle sending of messages"""
        user_input = self.entry_box.get().strip()
        if not user_input:
            return

        self.display_message(user_input, "User", "right")
        self.entry_box.delete(0, tk.END)

        response = self.process_query(user_input)
        self.display_message(response, "Bot", "left")

    def on_enter_pressed(self, event):
        """Handle Enter key press"""
        self.send_message()

    def display_message(self, message, sender, alignment):
        """Display a message in the chat area"""
        self.chat_area.config(state=tk.NORMAL)

        # Use different tags for user and bot messages
        tag = "user" if sender == "User" else "bot"
        self.chat_area.insert(tk.END, f"{sender}: ", tag)
        self.chat_area.insert(tk.END, f"{message}\n\n", tag)

        # Apply alignment
        tag_range = ("end-3l linestart", "end-2l lineend")
        self.chat_area.tag_add(alignment, *tag_range)

        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def process_query(self, user_input):
        user_input = user_input.strip()
        if not user_input:
            return "Please type something..."

        # Handle learning mode
        if self.awaiting_learning:
            if user_input and self.ml_model:
                success = self.ml_model.update_model(self.last_question, user_input)
                self.awaiting_learning = False
                return "Thanks, I've learned from that!" if success else "I couldn't learn that response."
            self.awaiting_learning = False
            return "Please provide a valid response to learn."

        # 1. Try ML model response
        if self.ml_model:
            try:
                ml_response = self.ml_model.get_response(user_input)
                if ml_response:
                    return ml_response
            except Exception as e:
                print(f"Error getting ML response: {e}")

        # 2. Try static responses
        processed = self.nlp_processor.preprocess(user_input)
        intent = self.nlp_processor.classify_intent(processed)
        static_response = self.chatbot.knowledge_base.get_static_response(intent)
        if static_response:
            return static_response

        # 3. Ask to teach
        self.awaiting_learning = True
        self.last_question = user_input
        return "I don't know how to answer that. What should I say?"

    def start_chat(self):
        """Start the chat interface"""
        self.master.mainloop()