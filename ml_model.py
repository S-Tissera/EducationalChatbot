from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import os
import re


class MLModel:
    def __init__(self, training_data=None, model_filename="chatbot_model.pkl"):
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            strip_accents='unicode',
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.model = MultinomialNB()
        self.model_filename = model_filename
        self.training_data = []
        self.trained = False
        self.similarity_threshold = 0.7
        self.vectorizer_fitted = False  # Track if vectorizer is fitted

        if os.path.exists(model_filename):
            self.load_model()
        elif training_data:
            self.initial_train(training_data)

    def clean_text(self, text):
        """Normalize text for consistent matching"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)
        return ' '.join(text.split())

    def initial_train(self, data):
        """Initial training with complete dataset"""
        self.training_data = [(self.clean_text(q), a) for q, a in data]
        questions = [q for q, _ in self.training_data]
        responses = [r for _, r in self.training_data]

        # Fit the vectorizer and model
        X = self.vectorizer.fit_transform(questions)
        self.vectorizer_fitted = True
        self.model.fit(X, responses)
        self.trained = True
        self.save_model()

    def find_similar_question(self, user_input):
        """Find semantically similar questions using cosine similarity"""
        if not self.training_data or not self.vectorizer_fitted:
            return None

        try:
            questions = [q for q, _ in self.training_data]
            question_vectors = self.vectorizer.transform(questions)
            input_vector = self.vectorizer.transform([user_input])

            similarities = cosine_similarity(input_vector, question_vectors)
            max_index = np.argmax(similarities)

            if similarities[0, max_index] > self.similarity_threshold:
                return self.training_data[max_index][1]
        except Exception as e:
            print(f"Similarity check error: {e}")
        return None

    def update_model(self, question, response):
        """Add new training example with semantic checking"""
        question = self.clean_text(question)
        response = response.strip()

        if not question or not response:
            return False

        # Check if similar question exists
        similar_answer = self.find_similar_question(question)
        if similar_answer:
            return True

        # Add new pair and retrain
        self.training_data.append((question, response))
        questions = [q for q, _ in self.training_data]
        responses = [r for _, r in self.training_data]

        # Refit vectorizer if not already fitted
        if not self.vectorizer_fitted:
            X = self.vectorizer.fit_transform(questions)
            self.vectorizer_fitted = True
        else:
            X = self.vectorizer.transform(questions)

        self.model.fit(X, responses)
        self.trained = True
        self.save_model()
        return True

    def get_response(self, user_input):
        """Get response using multiple matching strategies"""
        user_input = self.clean_text(user_input)

        # 1. Exact match
        for q, a in self.training_data:
            if q == user_input:
                return a

        # 2. Semantic similarity (only if vectorizer is fitted)
        if self.vectorizer_fitted:
            similar_answer = self.find_similar_question(user_input)
            if similar_answer:
                return similar_answer

        # 3. ML prediction
        if len(user_input.split()) >= 3 and self.vectorizer_fitted:
            try:
                X = self.vectorizer.transform([user_input])
                pred = self.model.predict(X)[0]
                proba = self.model.predict_proba(X).max()
                return pred if proba > 0.7 else None
            except Exception as e:
                print(f"Prediction error: {e}")

        return None

    def save_model(self):
        """Save complete model state"""
        model_data = {
            'vocabulary': self.vectorizer.vocabulary_ if self.vectorizer_fitted else None,
            'model': self.model,
            'training_data': self.training_data,
            'fitted': self.vectorizer_fitted
        }
        with open(self.model_filename, "wb") as f:
            pickle.dump(model_data, f)

    def load_model(self):
        """Load complete model state"""
        with open(self.model_filename, "rb") as f:
            data = pickle.load(f)
            self.vectorizer = TfidfVectorizer(
                vocabulary=data['vocabulary'],
                lowercase=True,
                strip_accents='unicode',
                stop_words='english',
                ngram_range=(1, 2)
            )
            self.model = data['model']
            self.training_data = data['training_data']
            self.vectorizer_fitted = data.get('fitted', False)
            self.trained = True


# Example training data (list of (question, response) tuples)
training_data = [
    ("hi", "Hello! How can I help you?"),
    ("hello", "Hi there! How can I assist you today?"),
    ("what courses are available", "We offer a variety of programs in IT, Business, and Arts."),
    ("what programs do you offer", "We offer programs in IT, Business, Arts, and Sciences."),
    ("how to apply", "You can apply through our website under the admissions section."),
    ("where can I apply", "You can apply via our online portal. Visit the admissions page."),
    ("what are the admission requirements", "You need to have a high school diploma and a good academic record."),
    ("what is the fee for the course",
     "The fee depends on the program. Please check the course details for more information."),
    ("how long does the course take", "Most courses are 3 to 4 years long, depending on the program."),
    ("what is the deadline for applications",
     "The application deadline is typically in June. Please refer to the admissions page for exact dates."),
    ("can I apply online", "Yes, applications are fully online through our website."),
    ("is there an entrance exam", "Some programs may require an entrance exam. Please check the program details."),
    (
    "how do I contact support", "You can contact support via email at support@example.com or by calling our helpline."),
    ("what is the program schedule", "The program schedule is flexible, with both part-time and full-time options."),
    ("can I get a scholarship",
     "Yes, scholarships are available based on merit. Please visit the scholarships page for more details."),
    ("do you offer online courses", "Yes, we offer a range of online courses. Visit our website for more information."),
    ("how can I get my transcript", "You can request your transcript through the student portal."),
    ("is there a student discount",
     "Yes, there are discounts available for students. You can check for discounts on the fee page."),
    ("what is the job placement rate",
     "Our job placement rate is very high, with many students securing jobs within six months of graduation."),
    ("can I defer my admission",
     "Yes, deferring your admission is possible. Please contact the admissions office for details."),
    ("do you offer internships",
     "Yes, we offer internships as part of our programs. Check the internship page for more details."),
    ("where are you located", "Our campus is located in the city center at 123 Main Street."),
    ("can I visit the campus", "Yes, we offer campus tours. Please contact the admissions office to schedule a visit."),
    ("is there a student club", "Yes, we have several student clubs ranging from academic to recreational interests."),
    ("can I change my major",
     "Yes, changing your major is possible within the first year. Speak with an academic advisor for guidance."),
    ("do you offer evening classes",
     "Yes, we offer evening classes for most programs. Please refer to the course schedule for availability."),
    ("are there work-study opportunities", "Yes, we offer work-study programs for eligible students."),
    ("how do I withdraw from a course",
     "To withdraw from a course, please visit the student portal or contact your academic advisor."),
    ("what is the grading system", "Our grading system is based on a 4.0 scale. An A is worth 4 points."),
    ("is there a deadline for dropping a course",
     "Yes, there is a deadline for course drops. Please refer to the academic calendar for dates."),
    (
    "how do I apply for a scholarship", "You can apply for a scholarship through the scholarship page on our website."),
    ("is there a fee for applying", "No, there is no application fee for most programs."),
    ("what is the admission process",
     "The admission process includes submitting an online application, academic transcripts, and meeting program requirements."),
    ("when will I receive my admission decision",
     "Admission decisions are typically made within 6-8 weeks after the application deadline."),
    ("can I apply for multiple programs",
     "Yes, you can apply for multiple programs, but each program has its own requirements."),
    ("is there an alumni network",
     "Yes, we have an alumni network that provides career support and networking opportunities."),
    ("do you offer part-time programs", "Yes, we offer part-time programs for working professionals."),
    ("how can I get a student ID",
     "You will receive a student ID during your orientation session after you're admitted."),
    ("where can I find course catalogs", "You can find course catalogs on the programs page on our website."),
    ("can I change my class schedule", "Yes, schedule changes are possible within the first week of classes."),
    ("do you offer a counseling service",
     "Yes, we provide student counseling services for academic and personal support."),
    ("is there a dress code", "There is no strict dress code, but we ask students to dress appropriately for class."),
    ("what is the campus environment like",
     "Our campus is very inclusive, with a vibrant student life and beautiful green spaces."),
    ("can I get a part-time job while studying",
     "Yes, many students work part-time while studying. Check with the career services office for opportunities."),
    ("how can I request a letter of recommendation",
     "You can request a letter of recommendation from your professors or academic advisors."),
    ("do you offer career counseling", "Yes, our career services offer counseling and job placement assistance."),
    ("is the campus accessible for disabled students",
     "Yes, our campus is fully accessible with ramps, elevators, and other facilities for disabled students."),
    ("do you offer language courses", "Yes, we offer language courses including English, Spanish, and French."),
    ("how do I check my grades", "You can check your grades on the student portal."),
    ("how do I reset my password",
     "You can reset your password by clicking the 'Forgot Password' link on the login page."),
]

# Initialize and train the model (or load it if it already exists)
ml_model = MLModel(training_data=training_data)