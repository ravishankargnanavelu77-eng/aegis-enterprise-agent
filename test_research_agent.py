from app.agents.research_agent import run_research_agent


task = """
Research external market conditions, enterprise technology
spending trends, cloud cost optimization behavior,
and competitive dynamics that could contribute to
a decline in enterprise software revenue.
"""

result = run_research_agent(task)

print("\n" + "=" * 60)
print("RESEARCH AGENT RESULT")
print("=" * 60)

print("\nSTATUS:")
print(result["status"])

print("\nANALYSIS:")
print(result["analysis"])

print("\nSOURCES:")
for source in result["sources"]:
    print(f"- {source['title']}")
    print(f"  {source['url']}")
