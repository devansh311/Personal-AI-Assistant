import streamlit as st
import uuid
from ui.session import save_threads

def render_sidebar():
    with st.sidebar:
        st.title("🤖 Personal AI Assistant")

        if st.button("+ New Chat"):
            thread_id = str(uuid.uuid4())
            st.session_state.threads[thread_id] = {"title": "New Chat"}
            save_threads(st.session_state.threads)

            # Update URL param so refresh keeps this thread
            st.query_params["thread"] = thread_id
            st.session_state.current_thread = thread_id
            st.rerun()

        st.divider()

        for thread_id, chat in st.session_state.threads.items():
            is_current = thread_id == st.session_state.current_thread
            label = f"{'▶ ' if is_current else ''}{chat['title']}"

            if st.button(label, key=thread_id):
                st.query_params["thread"] = thread_id
                st.session_state.current_thread = thread_id
                st.rerun()