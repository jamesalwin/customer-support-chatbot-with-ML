import streamlit as st
import pickle

# Load your model and data
model = pickle.load(open('chatbot_model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
intents = pickle.load(open('intents.pkl', 'rb'))

# Define function to get bot response
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

# Streamlit page setup
st.set_page_config(page_title="Customer Support Chatbot", page_icon="🤖")
st.title("🤖 Customer Support Chatbot")

# Session state to store conversation
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input field
user_input = st.text_input("Type your message:")

# Handle message submission
if st.button("Send") and user_input:
    reply = get_bot_response(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", reply))

# Display chat history
for sender, message in reversed(st.session_state.chat_history):
    st.markdown(f"**{sender}:** {message}")
