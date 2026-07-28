from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from rag.retriever import get_retriever
from config.llm import llm


def format_docs(docs):
    formatted = []

    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "Unknown")

        formatted.append(
            f"Source: {source}\n"
            f"Page: {page}\n\n"
            f"{doc.page_content}"
        )

    return "\n\n-----------------\n\n".join(formatted)


def get_rag_chain():
    retriever = get_retriever()

    prompt = ChatPromptTemplate.from_template(
        """
You are a helpful AI assistant.

Answer ONLY using the context provided below.

If the answer is not present in the context, say:
"I couldn't find that information in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""
    )

    chain = (
        {
            "context": retriever | format_docs,
            "question": lambda x: x,
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain