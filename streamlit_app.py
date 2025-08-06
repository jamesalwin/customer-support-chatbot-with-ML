import streamlit as st
import pickle

# Load trained components
model = pickle.load(open('chatbot_model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
intents = pickle.load(open('intents.pkl', 'rb'))

# Get bot response
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

# Streamlit UI setup
st.set_page_config(page_title="Customer Support Bot", page_icon="🤖")
st.title("🤖 Customer Support Chatbot")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input from user
user_msg = st.text_input("Type your message:", key="user_message")

if st.button("Send") or user_msg:
    if user_msg:
        reply = get_bot_response(user_msg)
        st.session_state.chat_history.append(("You", user_msg))
        st.session_state.chat_history.append(("Bot", reply))
        st.session_state.user_message = ""  # ✅ Reset user input field

# Display chat history
for sender, message in reversed(st.session_state.chat_history):
    st.write(f"**{sender}:** {message}")
