import streamlit as st
import requests

# FastAPI backend URL
FASTAPI_URL = "http://localhost:8000/query"

def get_response(user_input):
    response = requests.post(
        FASTAPI_URL,
        json={"session_id": "107", "input": user_input}
    )
    return response.json()["answer"]

st.title("Chat with SoftG")

user_input = st.text_input("You:", key="user_input")

if user_input:
    # Get AI response
    ai_response = get_response(user_input)
    st.write(ai_response)