import streamlit as st
import requests
import uuid
import streamlit.components.v1 as components

#Main Code
st.set_page_config(page_title="SoftG Chatbot", page_icon="🤖", layout="centered", initial_sidebar_state="auto")

if "session_id" not in st.session_state.keys():
    st.session_state.session_id = str(uuid.uuid4())

# BASE_URL='http://127.0.0.1:8000'
BASE_URL = "https://softgbotappservice.azurewebsites.net"
OPENAI_RESPONSE_URL = f"{BASE_URL}/query"
SESSION_DELETE_URL = f"{BASE_URL}/history/{st.session_state.session_id}"

#on window close event
delete_session_js = f"""
<script>
window.addEventListener('beforeunload', function (e) {{
    fetch('{SESSION_DELETE_URL}', {{
        method: 'DELETE'
    }});
}});
</script>
"""

components.html(delete_session_js, height=0, width=0)

#Functions
def start_new_chat():
    requests.delete(
        SESSION_DELETE_URL,
    )
    st.session_state.session_id = str(uuid.uuid4())
    clear_chat_history()

def get_response(session_id,user_input):
    payload = {"session_id": session_id, "input" : user_input}
    response = requests.post(
        OPENAI_RESPONSE_URL,
        json=payload
    )
    return response.json().get("answer", ["No response received"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hello ! How can I assist you today regarding our company Soft Gallery (PVT) LTD ?"}]


hide_menu_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

with st.sidebar:
    st.header('Welcome to SoftG Chatbot', divider= "blue")
    st.subheader('Options :')
    st.button('New  Chat', on_click=start_new_chat, help="Start a new chat session" , use_container_width=True)
    st.button('Clear Chat', on_click=clear_chat_history , help="Clear chat history", use_container_width=True)

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hello ! How can I assist you today regarding our company Soft Gallery (PVT) LTD ?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input(key="user_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("..."):
            session_id = st.session_state.session_id
            response = get_response(session_id, st.session_state.messages[-1]["content"])
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
