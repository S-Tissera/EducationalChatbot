import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Ensure punkt is downloaded
nltk.download('punkt')


class NLPProcessor:
    def __init__(self, db_manager):
        self.stemmer = PorterStemmer()
        self.db_manager = db_manager

    def preprocess(self, text):
        # Lowercase and remove punctuation from the input text
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        tokens = word_tokenize(text)  # Tokenize text
        return [self.stemmer.stem(word) for word in tokens]

    def classify_intent(self, processed_text):
        """
        Classifies the intent based on the processed text.
        Different keywords map to specific intents.
        """
        if any(word in processed_text for word in ["cours", "program", "subject", "field", "study", "degree"]):
            return "course_info"
        elif any(word in processed_text for word in ["admiss", "appli", "enrol", "register", "apply", "application"]):
            return "admission_info"
        elif any(word in processed_text for word in ["career", "job", "intern", "employ", "work", "placement"]):
            return "career_guidance"
        elif any(word in processed_text for word in ["scholar", "fund", "aid", "grant", "bursari", "scholarship"]):
            return "scholarship_info"
        elif any(
                word in processed_text for word in ["locat", "visit", "contact", "email", "address", "time", "campus"]):
            return "general_info"

        # Small Talk Intents
        elif any(word in processed_text for word in ["hi", "hello", "hey", "greetings"]):
            return "greeting"
        elif any(word in processed_text for word in ["bye", "goodbye", "see you", "later"]):
            return "goodbye"
        elif any(word in processed_text for word in ["how", "are", "you"]):
            return "how_are_you"
        elif any(word in processed_text for word in ["thank", "thanks"]):
            return "thank_you"
        elif any(word in processed_text for word in ["sorry", "apologize", "pardon"]):
            return "sorry"
        elif any(word in processed_text for word in ["help", "assist", "support", "need help"]):
            return "help"
        elif any(word in processed_text for word in ["name", "who are you", "what is your name"]):
            return "name"

        else:
            return "unknown"

    def get_response_from_db(self, intent):
        """
        Fetches the response based on the intent from the database.
        Returns either a static response from the knowledge base or a dynamic one from the DB.
        """
        # Query the database for the relevant response based on the intent
        response = self.db_manager.get_response_for_intent(intent)
        if response:
            return response
        else:
            return "Sorry, I don't have information on that topic."
