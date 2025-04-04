from education_chatbot.chatbotui import ChatbotUI
from education_chatbot.database_manager import DatabaseManager
from education_chatbot.inference_engine import Chatbot
from education_chatbot.knowledge_base import KnowledgeBase
from education_chatbot.ml_model import MLModel
from education_chatbot.nlp_processor import NLPProcessor

if __name__ == "__main__":
    # Database manager and knowledge base
    db_manager = DatabaseManager()  # Initialize the database manager
    knowledge_base = KnowledgeBase(db_manager)

    # NLP processor for text processing (pass db_manager to the constructor)
    nlp_processor = NLPProcessor(db_manager)

    # Initialize the ML model (load an existing model if available)
    #ml_model = MLModel()  # This will automatically load the model if it exists

    # Create the chatbot with the knowledge base, NLP processor, and ML model
    chatbot = Chatbot(knowledge_base, nlp_processor, """ml_model""")

    # Initialize the user interface
    ui = ChatbotUI(chatbot)

    # Start the chatbot conversation
    ui.start_chat()
