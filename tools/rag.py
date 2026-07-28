from langchain_core.tools import tool

from rag.chain import get_rag_chain

rag_chain = get_rag_chain()


@tool
def ask_documents(question: str) -> str:
    """
    Answer questions using the uploaded PDF documents.
    Use this tool whenever the user asks about notes, PDFs,
    uploaded files, resume, documentation, or study material.
    """

    return rag_chain.invoke(question)