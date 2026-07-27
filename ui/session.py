import uuid
import streamlit as st


def initialize_session():

    if "threads" not in st.session_state:
        st.session_state.threads = {}

    if "current_thread" not in st.session_state:

        thread_id = str(uuid.uuid4())

        st.session_state.current_thread = thread_id

        st.session_state.threads[thread_id] = {
            "title": "New Chat",
            "messages": []
        }