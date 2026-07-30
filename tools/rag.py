from langchain_core.tools import tool

from rag.chain import get_rag_chain

rag_chain = get_rag_chain()

@tool
def ask_documents(question: str) -> str:
    
    """
    Search uploaded PDF documents to answer questions.
    Use this tool ONLY when the user explicitly asks about
    content from their uploaded documents or files.
    Do NOT use this for general questions, greetings,
    coding syntax, math, weather, or anything not
    related to uploaded documents.
    Examples of when to use:
    - 'what does my notes say about BCNF'
    - 'summarize the uploaded PDF'
    - 'find information about X in my documents'
    Examples of when NOT to use:
    - 'hi', 'bye', 'cool', 'what is a priority queue'
    - 'what is the weather', 'calculate 5+5'
    """