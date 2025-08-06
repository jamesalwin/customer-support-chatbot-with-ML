import streamlit as st
import pickle
import base64

# Load the ML model and vectorizer
model = pickle.load(open('chatbot_model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
intents = pickle.load(open('intents.pkl', 'rb'))

# Bot response logic
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

# Function to load avatar image as base64
def load_avatar(file_path):
    with open(file_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

# Load avatars
bot_avatar = load_avatar("bot.png")
user_avatar = load_avatar("user.png")

# Custom CSS for chat bubbles
st.markdown("""
    <style>
    .chat-container {
        width: 100%;
        padding: 10px;
    }
    .message {
        display: flex;
        margin-bottom: 10px;
        align-items: flex-start;
    }
    .message.bot {
        flex-direction: row;
    }
    .message.user {
        flex-direction: row-reverse;
    }
    .message .bubble {
        max-width: 70%;
        padding: 10px 15px;
        border-radius: 12px;
        font-size: 16px;
        line-height: 1.4;
    }
    .message.bot .bubble {
        background-color: #e4e6eb;
        margin-left: 10px;
    }
    .message.user .bubble {
        background-color: #007bff;
        color: white;
        margin-right: 10px;
    }
    .message img {
        width: 40px;
        height: 40px;
        border-radius: 50%;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit layout
st.set_page_config(page_title="Customer Support Chatbot", page_icon="💬")
st.title("💬 Customer Support Chatbot")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("Type your message:")

# On send
if st.button("Send") and user_input:
    bot_response = get_bot_response(user_input)
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", bot_response))

# Render chat history with avatars
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for sender, message in st.session_state.chat_history:
    avatar = user_avatar if sender == "user" else bot_avatar
    sender_class = "user" if sender == "user" else "bot"
    
    chat_html = f"""
    <div class="message {sender_class}">
        <img src="data:image/png;base64,{avatar}" />
        <div class="bubble">{message}</div>
    </div>
    """
    st.markdown(chat_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
