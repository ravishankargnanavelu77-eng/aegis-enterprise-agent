from app.rag.retriever import retrieve_documents


query = (
    "What internal factors caused the "
    "Q2 enterprise revenue decline?"
)

results = retrieve_documents(query)

print("\n--- RETRIEVED DOCUMENTS ---\n")

for index, result in enumerate(results, start=1):
    print(f"RESULT {index}")
    print(f"Source: {result['source']}")
    print(result["content"])
    print("-" * 60)
