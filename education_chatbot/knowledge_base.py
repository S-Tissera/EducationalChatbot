import random

class KnowledgeBase:
    def __init__(self, database_manager):
        # Expanded static knowledge base with multiple responses for each intent
        self.static_data = {
            "admission_info": [
                "The admission process requires filling out an online form and submitting required documents. You must also upload your academic transcripts and a recommendation letter.",
                "To apply for admission, you need to submit an online application and provide your academic records and a recommendation letter.",
                "For admission, please fill out the form on our website and submit the required documents including transcripts and recommendation letters."
            ],
            "career_guidance": [
                "A degree in Computer Science can lead to careers in Software Development, Data Science, and AI Research. We also offer career counseling services and resume workshops.",
                "Computer Science graduates have great prospects in the tech industry, from software development to data analysis.",
                "If you're interested in a career in tech, a degree in Computer Science can open doors to software engineering, AI, and data science jobs."
            ],
            "course_info": [
                "We offer a wide range of programs including Computer Science, Business, Engineering, Arts, and Health Sciences. You can choose between full-time or part-time courses.",
                "Our university provides programs in fields like Computer Science, Business, Engineering, Arts, and more. You can study full-time or part-time.",
                "We have various degree programs in disciplines such as Engineering, Computer Science, Business, and more. You can pursue them full-time or part-time."
            ],
            "scholarship_info": [
                "Scholarships are awarded based on academic performance and financial need. You can apply for scholarships through our online portal. Specific eligibility requirements apply for each scholarship.",
                "We offer scholarships for students based on merit and financial need. You can apply for them through our website.",
                "Scholarships are available for students who meet certain academic and financial criteria. Please check our online portal for details."
            ],
            "general_info": [
                "Our campus is located at 456 Knowledge Blvd, Colombo. The campus is open Monday to Friday, from 9 AM to 5 PM. You can schedule a campus tour on our website.",
                "You can visit our campus at 456 Knowledge Blvd, Colombo, between 9 AM and 5 PM on weekdays. Tours are available by appointment.",
                "The campus is located at 456 Knowledge Blvd, Colombo, and is open from 9 AM to 5 PM Monday through Friday. You can book a campus tour online."
            ],
            "student_life": [
                "Student life at our university includes a range of extracurricular activities, clubs, and organizations. Students are encouraged to participate in events and make the most of their time on campus.",
                "We have a vibrant student life with various clubs, societies, and activities. You’ll have plenty of opportunities to meet new people and engage in extracurriculars.",
                "Our university offers a lively student experience, with numerous clubs, societies, and events to participate in throughout the year."
            ],
            "international_students": [
                "International students are welcome to apply. You will need to provide proof of English proficiency (TOEFL or IELTS), along with your academic transcripts. We also offer visa assistance for international students.",
                "We encourage international students to apply. You’ll need to show proof of English proficiency (TOEFL/IELTS) and your academic transcripts. We provide visa support as well.",
                "We welcome international students and offer assistance with visas and English proficiency requirements. Please provide TOEFL/IELTS scores and your transcripts."
            ],
            "application_deadlines": [
                "The application deadlines for each intake are January 31st for the Spring semester and August 31st for the Fall semester. Late applications may be considered on a case-by-case basis.",
                "Applications are due by January 31st for Spring and August 31st for Fall. We may consider late applications depending on the circumstances.",
                "The deadlines for application submission are January 31st for Spring and August 31st for Fall. Late applications are reviewed individually."
            ],
            "faculty_info": [
                "Our faculty members are highly qualified and experienced in their fields. You can view a list of faculty members on the university website under the 'Faculty' section.",
                "The faculty at our university are renowned experts in their fields. A list of faculty members is available on our website.",
                "Our professors are highly skilled and respected in their respective fields. You can find their details on our website under the 'Faculty' section."
            ],

            # Small Talk Responses
            "greeting": [
                "Hello! How can I assist you today?",
                "Hi there! How can I help you today?",
                "Hey! What can I do for you today?"
            ],
            "goodbye": [
                "Goodbye! Have a great day!",
                "Take care! Goodbye!",
                "See you later! Have a wonderful day!"
            ],
            "how_are_you": [
                "I'm just a chatbot, but I'm doing great! Thanks for asking.",
                "I'm doing great, thanks! How about you?",
                "I'm functioning perfectly, thank you! How can I assist you today?"
            ],
            "thank_you": [
                "You're welcome! Feel free to ask anything else.",
                "Glad I could help! Let me know if you need more assistance.",
                "No problem! Feel free to reach out anytime."
            ],
            "sorry": [
                "No worries! Let me know if you need help with anything else.",
                "It's okay! I'm here to help with anything you need.",
                "No problem at all! Feel free to ask me anything."
            ],
            "help": [
                "I'm here to assist with information about courses, admissions, scholarships, and more. How can I help you?",
                "I can assist you with course details, application processes, scholarships, and student life. How may I help?",
                "Need help? I can provide information on courses, scholarships, admissions, and much more."
            ],
            "name": [
                "I am your education counselor chatbot, here to assist with all your questions.",
                "My name is EduBot! I'm here to help you with all things education-related.",
                "I am EduBot, your personal education assistant. How can I assist you today?"
            ]
        }
        self.database_manager = database_manager

    def get_static_response(self, intent):
        # Select a random response from the list for the given intent
        responses = self.static_data.get(intent, None)
        if responses:
            return random.choice(responses)
        else:
            return None

    def fetch_dynamic_data(self, query):
        # Query the database for dynamic data based on the user input
        return self.database_manager.query_db(f"SELECT response FROM chatbot_data WHERE question='{query}'")
