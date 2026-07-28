
from langchain_openai import ChatOpenAI
from config.settings import OPENROUTER_API_KEY

import os

from config.settings import (
    OPENROUTER_API_KEY,
    LANGSMITH_API_KEY,
    LANGSMITH_TRACING,
    LANGSMITH_PROJECT
)

os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
os.environ["LANGSMITH_TRACING"] = LANGSMITH_TRACING
os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT

llm = ChatOpenAI(
    model="openrouter/free",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    streaming=False
)