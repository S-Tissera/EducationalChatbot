import random
from typing import Dict, List, Optional


class KnowledgeBase:
    def __init__(self, database_manager=None):
        """
        Initialize the knowledge base with protected intents and static responses.

        Args:
            database_manager: Optional database connection manager
        """
        self.database_manager = database_manager
        self.protected_intents = {
            'greeting',
            'how_are_you',
            'goodbye',
            'thank_you',
            'sorry',
            'help',
            'name'
        }

        self.static_data: Dict[str, List[str]] = {
            # Academic Information
            "course_info": [
                "We offer undergraduate and graduate programs in Computer Science, Business Administration, and Engineering.",
                "Our available courses include Computer Science, Electrical Engineering, and MBA programs. Visit our website for details.",
                "You can choose from various programs including Data Science, Artificial Intelligence, and Business Analytics."
            ],
            "admission_info": [
                "The admission process requires an online application, academic transcripts, and two recommendation letters.",
                "To apply, complete our online application form and submit your academic records. Deadline is May 15th.",
                "Admissions are open for Fall 2023. Requirements include a 3.0 GPA and English proficiency test for international students."
            ],
            "scholarship_info": [
                "We offer merit-based scholarships covering up to 50% of tuition. Application deadline is March 1st.",
                "Financial aid options include need-based grants and athletic scholarships. Complete the FAFSA for consideration.",
                "The university provides several scholarship opportunities based on academic excellence and community service."
            ],

            # Campus Life
            "campus_facilities": [
                "Our campus features state-of-the-art labs, a modern library, and sports complexes open 7am-10pm daily.",
                "Facilities include computer labs, research centers, and a student recreation center with a swimming pool.",
                "You'll find excellent facilities including 24/7 study spaces, cafeterias, and fitness centers across campus."
            ],
            "student_activities": [
                "We have over 100 student clubs including robotics, debate, and cultural organizations.",
                "Student life includes weekly events, guest lectures, and annual festivals like our Spring Carnival.",
                "There are many extracurricular activities ranging from academic clubs to intramural sports teams."
            ],

            # Administrative
            "registration_info": [
                "Course registration opens April 1st for continuing students and June 1st for new students.",
                "You can register for classes through the student portal during your assigned registration period.",
                "Registration requires meeting with your academic advisor first to get your PIN for the system."
            ],
            "tuition_info": [
                "Undergraduate tuition is $15,000 per semester. Financial aid options are available.",
                "Tuition varies by program. Graduate programs range from $20,000-$25,000 per academic year.",
                "You can view the complete tuition breakdown on our website under the 'Costs & Aid' section."
            ],

            # Small Talk
            "greeting": [
                "Hello! Welcome to University Chatbot. How can I assist you today?",
                "Hi there! I'm here to help with any questions about our university.",
                "Greetings! What would you like to know about our programs and campus?"
            ],
            "how_are_you": [
                "I'm functioning perfectly, thank you! How can I help you today?",
                "Doing great! Ready to answer your questions about the university.",
                "I'm just a chatbot, but I'm happy to assist with your inquiries!"
            ],
            "goodbye": [
                "Goodbye! Feel free to come back if you have more questions.",
                "Have a wonderful day! Contact us anytime if you need assistance.",
                "See you later! Don't hesitate to ask if you need more information."
            ],
            "thank_you": [
                "You're welcome! Let me know if you need anything else.",
                "Happy to help! Don't hesitate to ask more questions.",
                "My pleasure! Feel free to ask about other topics too."
            ],

            # Error Handling
            "unknown": [
                "I'm not sure I understand. Could you rephrase your question?",
                "I don't have information about that. Try asking about admissions, courses, or campus life.",
                "That's not something I can help with. I specialize in university information."
            ]
        }

    def get_static_response(self, intent: str) -> Optional[str]:
        """
        Get a random response for the given intent if it exists.

        Args:
            intent: The classified intent of the user's query

        Returns:
            A random response string or None if intent not found
        """
        responses = self.static_data.get(intent)
        return random.choice(responses) if responses else None

    def fetch_dynamic_data(self, query: str) -> Optional[str]:
        """
        Query the database for dynamic responses if a database manager is available.

        Args:
            query: The user's original question

        Returns:
            Response from database or None if not found
        """
        if not self.database_manager:
            return None

        try:
            # Use parameterized query to prevent SQL injection
            result = self.database_manager.query_db(
                "SELECT response FROM chatbot_responses WHERE question = %s",
                (query,)
            )
            return result[0] if result else None
        except Exception as e:
            print(f"Database query error: {e}")
            return None

    def is_protected_intent(self, intent: str) -> bool:
        """
        Check if an intent is protected from being overwritten by learned responses.

        Args:
            intent: The intent to check

        Returns:
            True if the intent is protected, False otherwise
        """
        return intent in self.protected_intents