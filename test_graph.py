from app.graph.workflow import build_graph


graph = build_graph()

print("=" * 60)
print("AEGIS ENTERPRISE AI AGENT")
print("=" * 60)

query = input("\nEnter your enterprise analysis question:\n> ").strip()

if not query:
    print("\nNo query entered. Please run the program again.")
    raise SystemExit(1)

print("\n" + "=" * 60)
print("PROCESSING YOUR QUERY")
print("=" * 60)

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
