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

# Streamlit UI
st.set_page_config(page_title="Customer Support Bot", page_icon="💬")
st.title("🤖 Customer Support Chatbot")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Type your message:", key="input")

if st.button("Send") or user_input:
    if user_input:
        reply = get_bot_response(user_input)
        st.session_state.chat.append(("You", user_input))
        st.session_state.chat.append(("Bot", reply))
        st.session_state.input = ""

for sender, message in reversed(st.session_state.chat):
    st.write(f"**{sender}:** {message}")
