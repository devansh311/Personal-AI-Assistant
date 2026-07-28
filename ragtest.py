from rag.retriever import get_retriever

retriever = get_retriever()

docs = retriever.invoke("Explain paging")

print(f"Retrieved {len(docs)} documents\n")

for i, doc in enumerate(docs, 1):
    print("=" * 60)
    print(doc.metadata)
    print(doc.page_content[:500])