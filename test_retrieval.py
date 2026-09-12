from rag import (
    load_documents,
    split_documents,
    add_database_schema,
    create_vector_store
)


# 1. Load PDF + runbooks
documents = load_documents()

print("Documents loaded:", len(documents))


# 2. Add PostgreSQL schema
documents = add_database_schema(documents)

print("Documents after schema:", len(documents))


# 3. Split into chunks
chunks = split_documents(documents)

print("Chunks created:", len(chunks))


# 4. Create vector store
vector_store = create_vector_store(chunks)

print("Vector store created successfully!")


# 5. Test retrieval
question = "What should I check when PostgreSQL CPU is high?"

results = vector_store.similarity_search(
    question,
    k=3
)


print("\n====================================")
print("RETRIEVED KNOWLEDGE")
print("====================================")


for i, doc in enumerate(results):

    print("\n------------------------------------")
    print("RESULT:", i + 1)

    print("SOURCE:")
    print(doc.metadata)

    print("\nCONTENT:")
    print(doc.page_content)