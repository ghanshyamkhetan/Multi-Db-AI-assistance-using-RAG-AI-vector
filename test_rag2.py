from rag import load_documents


documents = load_documents()

print("\n====================================")
print("RAG DOCUMENT LOADING TEST")
print("====================================")

print("Total documents/pages loaded:", len(documents))


for i, doc in enumerate(documents):

    print("\n------------------------------------")
    print("DOCUMENT:", i + 1)
    print("SOURCE:", doc.metadata.get("source"))
    print("PAGE:", doc.metadata.get("page"))
    print("TEXT LENGTH:", len(doc.page_content))

    print("\nTEXT PREVIEW:")
    print(doc.page_content[:300])