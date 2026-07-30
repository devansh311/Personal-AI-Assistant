import uuid
import json
import os
import streamlit as st

THREADS_FILE = "database/threads.json"

def load_threads():
    os.makedirs("database", exist_ok=True)
    if os.path.exists(THREADS_FILE):
        with open(THREADS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_threads(threads):
    os.makedirs("database", exist_ok=True)
    with open(THREADS_FILE, "w") as f:
        json.dump(threads, f)


def initialize_session():
    # Load persisted threads from file on every refresh
    if "threads" not in st.session_state:
        st.session_state.threads = load_threads()

    # Get or create thread_id from URL params
    params = st.query_params

    if "thread" not in params:
        thread_id = str(uuid.uuid4())
        params["thread"] = thread_id
    
    thread_id = params["thread"]
    st.session_state.current_thread = thread_id

    # Add to threads dict if new
    if thread_id not in st.session_state.threads:
        st.session_state.threads[thread_id] = {"title": "New Chat"}
        save_threads(st.session_state.threads)