from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os


class MLModel:
    def __init__(self, training_data=None, model_filename="chatbot_model.pkl"):
        self.vectorizer = CountVectorizer()
        self.model = MultinomialNB()

        # Check if a saved model exists, and load it if available
        if os.path.exists(model_filename):
            self.load_model(model_filename)
        elif training_data:
            # If no saved model, train a new one with the provided data
            self.train(training_data, model_filename)

    def train(self, data, model_filename="chatbot_model.pkl"):
        questions, responses = zip(*data)
        X = self.vectorizer.fit_transform(questions)
        self.model.fit(X, responses)

        # Save the model after training
        self.save_model(model_filename)

    def predict_response(self, user_input):
        X_input = self.vectorizer.transform([user_input])
        return self.model.predict(X_input)[0]

    def save_model(self, filename="chatbot_model.pkl"):
        with open(filename, "wb") as f:
            pickle.dump((self.vectorizer, self.model), f)

    def load_model(self, filename="chatbot_model.pkl"):
        with open(filename, "rb") as f:
            self.vectorizer, self.model = pickle.load(f)


# Example training data
training_data = [
    ("hi", "Hello! How can I help you?"),
    ("hello", "Hi there! How can I assist you today?"),
    ("what courses are available", "We offer a variety of programs in IT, Business, and Arts."),
    ("what programs do you offer", "We offer programs in IT, Business, Arts, and Sciences."),
    ("how to apply", "You can apply through our website under the admissions section."),
    ("where can I apply", "You can apply via our online portal. Visit the admissions page."),
    ("what are the admission requirements", "You need to have a high school diploma and a good academic record."),
    ("what is the fee for the course", "The fee depends on the program. Please check the course details for more information."),
    ("how long does the course take", "Most courses are 3 to 4 years long, depending on the program."),
    ("what is the deadline for applications", "The application deadline is typically in June. Please refer to the admissions page for exact dates."),
    ("can I apply online", "Yes, applications are fully online through our website."),
    ("is there an entrance exam", "Some programs may require an entrance exam. Please check the program details."),
    ("how do I contact support", "You can contact support via email at support@example.com or by calling our helpline."),
    ("what is the program schedule", "The program schedule is flexible, with both part-time and full-time options."),
    ("can I get a scholarship", "Yes, scholarships are available based on merit. Please visit the scholarships page for more details."),
    ("do you offer online courses", "Yes, we offer a range of online courses. Visit our website for more information."),
    ("how can I get my transcript", "You can request your transcript through the student portal."),
    ("is there a student discount", "Yes, there are discounts available for students. You can check for discounts on the fee page."),
    ("what is the job placement rate", "Our job placement rate is very high, with many students securing jobs within six months of graduation."),
    ("can I defer my admission", "Yes, deferring your admission is possible. Please contact the admissions office for details."),
    ("do you offer internships", "Yes, we offer internships as part of our programs. Check the internship page for more details."),
    ("where are you located", "Our campus is located in the city center at 123 Main Street."),
    ("can I visit the campus", "Yes, we offer campus tours. Please contact the admissions office to schedule a visit."),
    ("is there a student club", "Yes, we have several student clubs ranging from academic to recreational interests."),
    ("can I change my major", "Yes, changing your major is possible within the first year. Speak with an academic advisor for guidance."),
    ("do you offer evening classes", "Yes, we offer evening classes for most programs. Please refer to the course schedule for availability."),
    ("are there work-study opportunities", "Yes, we offer work-study programs for eligible students."),
    ("how do I withdraw from a course", "To withdraw from a course, please visit the student portal or contact your academic advisor."),
    ("what is the grading system", "Our grading system is based on a 4.0 scale. An A is worth 4 points."),
    ("is there a deadline for dropping a course", "Yes, there is a deadline for course drops. Please refer to the academic calendar for dates."),
    ("how do I apply for a scholarship", "You can apply for a scholarship through the scholarship page on our website."),
    ("is there a fee for applying", "No, there is no application fee for most programs."),
    ("what is the admission process", "The admission process includes submitting an online application, academic transcripts, and meeting program requirements."),
    ("when will I receive my admission decision", "Admission decisions are typically made within 6-8 weeks after the application deadline."),
    ("can I apply for multiple programs", "Yes, you can apply for multiple programs, but each program has its own requirements."),
    ("is there an alumni network", "Yes, we have an alumni network that provides career support and networking opportunities."),
    ("do you offer part-time programs", "Yes, we offer part-time programs for working professionals."),
    ("how can I get a student ID", "You will receive a student ID during your orientation session after you’re admitted."),
    ("where can I find course catalogs", "You can find course catalogs on the programs page on our website."),
    ("can I change my class schedule", "Yes, schedule changes are possible within the first week of classes."),
    ("do you offer a counseling service", "Yes, we provide student counseling services for academic and personal support."),
    ("is there a dress code", "There is no strict dress code, but we ask students to dress appropriately for class."),
    ("what is the campus environment like", "Our campus is very inclusive, with a vibrant student life and beautiful green spaces."),
    ("can I get a part-time job while studying", "Yes, many students work part-time while studying. Check with the career services office for opportunities."),
    ("how can I request a letter of recommendation", "You can request a letter of recommendation from your professors or academic advisors."),
    ("do you offer career counseling", "Yes, our career services offer counseling and job placement assistance."),
    ("is the campus accessible for disabled students", "Yes, our campus is fully accessible with ramps, elevators, and other facilities for disabled students."),
    ("do you offer language courses", "Yes, we offer language courses including English, Spanish, and French."),
    ("how do I check my grades", "You can check your grades on the student portal."),
    ("how do I reset my password", "You can reset your password by clicking the 'Forgot Password' link on the login page."),
]


# Initialize and train the model (or load it if it already exists)
ml_model = MLModel(training_data=training_data)
