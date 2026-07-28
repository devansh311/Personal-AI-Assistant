import streamlit as st

from backend import chatbot
from langchain_core.messages import HumanMessage

from ui.session import initialize_session
from ui.sidebar import render_sidebar

from utils.formatter import extract_text

# ------------------ PAGE CONFIG ------------------ #

st.set_page_config(
    page_title="Personal AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ------------------ INITIALIZE ------------------ #

initialize_session()

render_sidebar()

# Current Chat
current_chat = st.session_state.threads[
    st.session_state.current_thread
]

CONFIG = {
    "configurable": {
        "thread_id": st.session_state.current_thread
    }
}

# ------------------ TITLE ------------------ #

st.title("🤖 Personal AI Assistant")

# ------------------ DISPLAY OLD MESSAGES ------------------ #

for msg in current_chat["messages"]:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# ------------------ USER INPUT ------------------ #

query = st.chat_input("Ask anything...")
if query:

    # Store user message
    current_chat["messages"].append(
        {
            "role": "user",
            "content": query
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(query)

    # Invoke chatbot
    result = chatbot.invoke(
        {
            "messages": [
                HumanMessage(content=query)
            ]
        },
        config=CONFIG
    )

    answer = result["messages"][-1].content

    # Store assistant message
    current_chat["messages"].append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(answer)