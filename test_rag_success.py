from rag import load_documents


documents = load_documents()

print("Number of documents:", len(documents))

for doc in documents:

    print("\n-------------------------")
    print("SOURCE:")
    print(doc.metadata)

    print("\nCONTENT:")
    print(doc.page_content[:500])