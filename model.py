import pickle

model = pickle.load(open('chatbot_model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
intents = pickle.load(open('intents.pkl', 'rb'))

def get_bot_response(user_input):
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    if user_input.lower() in greetings:
        return "Hello! How can I assist you today?"

    X = vectorizer.transform([user_input])
    intent_tag = model.predict(X)[0]

    for intent in intents['intents']:
        if intent['tag'] == intent_tag:
            return intent['responses'][0]

    return "Sorry, I didn't understand that."
