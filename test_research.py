from app.services.research import search_web


query = (
    "enterprise software market trends "
    "cloud spending budget pressure 2026"
)

results = search_web(
    query=query,
    max_results=3,
)

print("\n--- RESEARCH RESULTS ---\n")

for index, result in enumerate(results, start=1):
    print(f"RESULT {index}")
    print(f"TITLE: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"CONTENT: {result['content'][:500]}")
    print("-" * 70)
