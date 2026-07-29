import os
import streamlit as st

from backend import chatbot
from langchain_core.messages import HumanMessage
from langgraph.types import Command

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

# ------------------ PDF UPLOAD ------------------ #

st.sidebar.divider()
st.sidebar.subheader("📄 Upload Documents")

uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file is not None:
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", uploaded_file.name)

    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success(f"✅ {uploaded_file.name} uploaded successfully!")
    else:
        st.sidebar.info("📁 This PDF already exists.")

# ------------------ CURRENT CHAT ------------------ #

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

    # Store and display user message
    current_chat["messages"].append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Check if graph is currently interrupted (waiting for confirmation)
    graph_state = chatbot.get_state(CONFIG)
    is_interrupted = bool(
        graph_state.tasks and
        any(task.interrupts for task in graph_state.tasks)
    )

    if is_interrupted:
        # Graph is paused — resume it with user's response
        result = chatbot.invoke(
            Command(resume=query),
            config=CONFIG
        )
    else:
        # Normal flow — send as new message
        result = chatbot.invoke(
            {"messages": [HumanMessage(content=query)]},
            config=CONFIG
        )

    # Check if graph paused AFTER this invoke (new interrupt)
    new_state = chatbot.get_state(CONFIG)
    new_interrupt = bool(
        new_state.tasks and
        any(task.interrupts for task in new_state.tasks)
    )

    if new_interrupt:
        # Graph paused — show interrupt confirmation message to user
        for task in new_state.tasks:
            if task.interrupts:
                interrupt_msg = task.interrupts[0].value

                current_chat["messages"].append({
                    "role": "assistant",
                    "content": interrupt_msg
                })

                with st.chat_message("assistant"):
                    st.markdown(interrupt_msg)
                break
    else:
        # Normal response — get last AI message
        answer = extract_text(result["messages"][-1])

        current_chat["messages"].append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.markdown(answer)