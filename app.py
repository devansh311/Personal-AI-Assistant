import os
import streamlit as st

from backend import chatbot
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from ui.session import initialize_session, save_threads
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

uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", uploaded_file.name)

    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success(f"✅ {uploaded_file.name} uploaded successfully!")
    else:
        st.sidebar.info("📁 This PDF already exists.")

# ------------------ CONFIG ------------------ #

CONFIG = {
    "configurable": {
        "thread_id": st.session_state.current_thread
    }
}

# ------------------ TITLE ------------------ #

st.title("🤖 Personal AI Assistant")

# ------------------ DISPLAY MESSAGES FROM POSTGRESQL ------------------ #

graph_state = chatbot.get_state(CONFIG)
messages = graph_state.values.get("messages", [])

for msg in messages:
    if msg.type == "human":
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif msg.type == "ai" and msg.content:
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# ------------------ USER INPUT ------------------ #

query = st.chat_input("Ask anything...")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    # Auto-update thread title from first message
    current_thread = st.session_state.current_thread
    if st.session_state.threads[current_thread]["title"] == "New Chat":
        title = query[:30] + "..." if len(query) > 30 else query
        st.session_state.threads[current_thread]["title"] = title
        save_threads(st.session_state.threads)

    # Check if graph is interrupted
    graph_state = chatbot.get_state(CONFIG)
    is_interrupted = bool(
        graph_state.tasks and
        any(task.interrupts for task in graph_state.tasks)
    )

    if is_interrupted:
        result = chatbot.invoke(Command(resume=query), config=CONFIG)
    else:
        result = chatbot.invoke(
            {"messages": [HumanMessage(content=query)]},
            config=CONFIG
        )

    # Check if new interrupt happened
    new_state = chatbot.get_state(CONFIG)
    new_interrupt = bool(
        new_state.tasks and
        any(task.interrupts for task in new_state.tasks)
    )

    if new_interrupt:
        for task in new_state.tasks:
            if task.interrupts:
                interrupt_msg = task.interrupts[0].value
                with st.chat_message("assistant"):
                    st.markdown(interrupt_msg)
                break
    else:
        answer = extract_text(result["messages"][-1])
        with st.chat_message("assistant"):
            st.markdown(answer)