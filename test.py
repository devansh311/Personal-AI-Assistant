from config.llm import llm

print("Sending request...")

response = llm.invoke("Say hello in one sentence.")

print(response.content)