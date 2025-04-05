import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Ensure punkt is downloaded
nltk.download('punkt', quiet=True)

class NLPProcessor:
    def __init__(self, db_manager=None):
        self.stemmer = PorterStemmer()
        self.db_manager = db_manager

    def preprocess(self, text):
        """Preprocess text by lowercasing, removing punctuation, and stemming"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        tokens = word_tokenize(text)
        return [self.stemmer.stem(word) for word in tokens]

    def classify_intent(self, processed_text):
        """More precise intent classification"""
        # Check for greeting patterns first
        greeting_words = ["hi", "hello", "hey", "greet"]
        if any(word in processed_text for word in greeting_words):
            return "greeting"

        # Check for "how are you" separately
        if all(word in processed_text for word in ["how", "are", "you"]):
            return "how_are_you"



        # Rest of your intent matching...
        intent_keywords = {
            "course_info": ["cours", "program", "subject", "field", "study", "degree"],
            "admission_info": ["admiss", "appli", "enrol", "register", "apply", "application"],
            "career_guidance": ["career", "job", "intern", "employ", "work", "placement"],
            "scholarship_info": ["scholar", "fund", "aid", "grant", "bursari", "scholarship"],
            "general_info": ["locat", "visit", "contact", "email", "address", "time", "campus"],
            "greeting": ["hi", "hello", "hey", "greetings"],
            "goodbye": ["bye", "goodbye", "see you", "later"],
            "how_are_you": ["how", "are", "you"],
            "thank_you": ["thank", "thanks"],
            "sorry": ["sorry", "apologize", "pardon"],
            "help": ["help", "assist", "support", "need help"],
            "contact_info": ["contact", "reach", "get in touch", "speak to"],
            "phone_number": ["phone", "number", "call", "telephone"],
            "name": ["name", "who are you", "what is your name"]
        }

        for intent, keywords in intent_keywords.items():
            if any(keyword in processed_text for keyword in keywords):
                return intent
        return "unknown"

    def get_response_from_db(self, intent):
        """Get response from database or return default if not found"""
        if self.db_manager:
            response = self.db_manager.get_response_for_intent(intent)
            if response:
                return response
        return "Sorry, I don't have information on that topic."