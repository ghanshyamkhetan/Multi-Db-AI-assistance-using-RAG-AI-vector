from asistant import ask_database

question = """
What should I check when PostgreSQL CPU is high?
"""

response = ask_database(question)

print("\nSQL:")
print(response["sql"])

print("\nRESULT:")
print(response["result"])