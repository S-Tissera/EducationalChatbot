from education_chatbot.chatbotui import ChatbotUI
from education_chatbot.database_manager import DatabaseManager
from education_chatbot.inference_engine import Chatbot
from education_chatbot.knowledge_base import KnowledgeBase
from education_chatbot.ml_model import MLModel
from education_chatbot.nlp_processor import NLPProcessor
import tkinter as tk
import os

if __name__ == "__main__":
    try:
        # Initialize components
        db_manager = DatabaseManager()
        knowledge_base = KnowledgeBase(db_manager)
        nlp_processor = NLPProcessor(db_manager)

        ml_model = MLModel()

        # Create chatbot instance
        chatbot = Chatbot(knowledge_base, nlp_processor, ml_model)

        # Create and run UI
        root = tk.Tk()
        ui = ChatbotUI(root, chatbot, nlp_processor, ml_model)
        ui.start_chat()

    except Exception as e:
        print(f"Application error: {e}")
