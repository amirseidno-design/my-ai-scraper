import os

print("Hello! The robot is working.")
print("Secret loaded:", os.getenv("GROQ_API_KEY") is not None)
