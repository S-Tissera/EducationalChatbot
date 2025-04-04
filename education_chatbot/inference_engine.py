class Chatbot:
    def __init__(self, knowledge_base, nlp_processor, ml_model=None):
        self.knowledge_base = knowledge_base
        self.nlp_processor = nlp_processor
        self.ml_model = ml_model  # Optional

    def process_query(self, user_input):
        cleaned_input = self.nlp_processor.preprocess(user_input)
        intent = self.nlp_processor.classify_intent(cleaned_input)

        # Check for static responses first
        response = self.knowledge_base.get_static_response(intent)
        if response:
            return response

        # Fetch dynamic data if no static response
        response = self.knowledge_base.fetch_dynamic_data(intent)
        if response:
            return response

        # If ML model is available, use it to generate responses
        if self.ml_model:
            return self.ml_model.predict_response(user_input)

        return "I'm sorry, I don't have information on that topic."

