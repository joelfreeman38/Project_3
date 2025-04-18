# Placeholder Good Mental Health Chatbot

# To run streamlit app, navigate to BadChatbot folder and enter 'streamlit run BadChatbot_streamlit.py'. Install requirements.txt modules if necessary.
# 🚨 Disable TensorFlow usage to avoid Keras 3 incompatibility
import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

import streamlit as st
from transformers import pipeline
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableSequence
from langchain.prompts import ChatPromptTemplate


# --- UI Setup ---
st.title("🧘‍♀️ Good Mental Health Chatbot")
st.write("DISCLAIMER: This is for instructional purposes only. Do not follow this chatbot's advice!")

# Sidebar for Gemini API key
st.sidebar.title("Configuration")
GEMINI_API_KEY = st.sidebar.text_input("Enter your Gemini API key", type="password")

# --- Model Setup ---
# Load sentiment analysis pipeline
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    framework="pt"  # <-- Force PyTorch backend
)

# Define the Gemini model name
GEMINI_MODEL = "gemini-1.5-flash"  # Added this line to define the model

# Define prompt
prompt_template = ChatPromptTemplate.from_template(
    "You are a good cognitive behavioral therapist "
    "The user said: '{user_input}'. Sentiment analysis result: {sentiment}. "
    "Tell the user the sentiment you detected, and respond with advice like a good therapist would. "
)

# Define chatbot response function
def analyze_and_respond(user_input, chat_chain):
    sentiment_result = sentiment_analyzer(user_input)[0]
    label = sentiment_result['label']
    score = sentiment_result['score']

    if label == "POSITIVE" and score > 0.70:
        sentiment = "positive"
    elif label == "NEGATIVE" and score > 0.70:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    response_obj = chat_chain.invoke({"user_input": user_input, "sentiment": sentiment})
    return response_obj.content
    
# --- Main App Logic ---
if GEMINI_API_KEY:
    user_input = st.text_input("So what's going on with you?")

    if st.button("Get Advice"):
        if not user_input:
            st.warning("I'm here for you!")
        else:
            try:
                llm = ChatGoogleGenerativeAI(
                    model=GEMINI_MODEL,
                    google_api_key=GEMINI_API_KEY,
                    temperature=0.9
                )
                chat_chain = RunnableSequence(prompt_template | llm)

                response = analyze_and_respond(user_input, chat_chain)

                st.markdown("**Response:**")
                st.write(response)
            except Exception as e:
                st.error(f"Something went wrong, you idiot! Error: {str(e)}")
else:
    st.info("Please enter your Gemini API key in the sidebar to continue.")