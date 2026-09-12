from langchain_community.document_loaders import PyPDFLoader

pdf_path = "knowledge/postgres/postgres_admin.pdf"

loader = PyPDFLoader(pdf_path)

documents = loader.load()

print("Number of PDF pages:", len(documents))

for doc in documents:
    print("\n-------------------------")
    print("PAGE:", doc.metadata.get("page"))
    print("SOURCE:", doc.metadata.get("source"))
    print("TEXT LENGTH:", len(doc.page_content))
    print(doc.page_content[:500])