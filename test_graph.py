from app.graph.workflow import build_graph


graph = build_graph()

query = (
    "Why did enterprise revenue decline in Q2? "
    "Analyze internal revenue data by region, product, and customer segment. "
    "Search internal company documents for operational explanations. "
    "Also research external market conditions, enterprise software spending trends, "
    "cloud cost optimization trends, and competitive dynamics that may have "
    "contributed to the revenue decline."
)

result = graph.invoke(
    {
        "query": query
    }
)

print("\n" + "=" * 60)
print("FINAL RESULT")
print("=" * 60)

print(result["final_answer"])

print("\n--- EXECUTION PLAN ---")

for task in result["execution_plan"]:
    print(f"\n{task['id']} → {task['agent'].upper()}")
    print(task["description"])

print("\n" + "=" * 60)
print("AGENT RESULTS")
print("=" * 60)

for task_id, agent_result in result["agent_results"].items():
    print(f"\n{task_id}")
    print(agent_result)