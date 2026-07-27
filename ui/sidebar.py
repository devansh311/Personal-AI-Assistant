import streamlit as st
import uuid


def render_sidebar():

    with st.sidebar:

        st.title("🤖 Personal AI")

        if st.button("+ New Chat"):

            thread_id = str(uuid.uuid4())

            st.session_state.threads[thread_id] = {
                "title": "New Chat",
                "messages": []
            }

            st.session_state.current_thread = thread_id

            st.rerun()

        st.divider()

        for thread_id, chat in st.session_state.threads.items():

            if st.button(chat["title"], key=thread_id):

                st.session_state.current_thread = thread_id

                st.rerun()