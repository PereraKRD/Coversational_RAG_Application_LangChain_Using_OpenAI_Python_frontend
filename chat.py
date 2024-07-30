import streamlit as st
import requests

FASTAPI_URL = "https://softgbotappservice.azurewebsites.net/query"

st.set_page_config(page_title="SoftG Chatbot")

hide_menu_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

with st.sidebar:
    st.header('Configuration')
    session_id = st.text_input("Session ID", value = 'default-session')

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

def get_response(session_id,user_input):
    payload = {"session_id": session_id, "input" : user_input}
    response = requests.post(
        FASTAPI_URL,
        json=payload
    )
    return response.json().get("answer","No response recieved")

if prompt := st.chat_input(key="user_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("..."):
            response = get_response(session_id,prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
