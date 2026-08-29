from app.agents.planner import create_execution_plan


query = (
    "Why did enterprise revenue decline in Q2, "
    "and what external market factors may have contributed?"
)

plan = create_execution_plan(query)

print("\n--- EXECUTION PLAN ---")
print(f"Goal: {plan.goal}\n")

for task in plan.tasks:
    print(f"Task ID: {task.id}")
    print(f"Agent: {task.agent}")
    print(f"Description: {task.description}")
    print()
