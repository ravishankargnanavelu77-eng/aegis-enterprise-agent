from app.services.llm import get_llm


llm = get_llm()

response = llm.invoke(
    "Reply with exactly this sentence: Aegis AI is running successfully."
)

print(response.content)
