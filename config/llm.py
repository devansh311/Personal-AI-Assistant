import os
from langchain_groq import ChatGroq
from config.settings import (
    GROQ_API_KEY,
    LANGSMITH_API_KEY,
    LANGSMITH_TRACING,
    LANGSMITH_PROJECT
)

os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
os.environ["LANGSMITH_TRACING"] = LANGSMITH_TRACING
os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
    temperature=0
)