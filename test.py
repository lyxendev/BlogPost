from openai import OpenAI
import os
from dotenv import load_dotenv

# ==================== LOAD API KEY FROM .env ====================
load_dotenv()  # .env loading

API_KEY = os.getenv("GROQ_API_KEY")

# Check if API key exists
if not API_KEY:
    print(f"❌ API key not found! Please check your .env file.")
    print(f"Create a .env file with: GROQ_API_KEY=your_key_here")
    exit()

# Groq API setup
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=API_KEY
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
		{"role": "user", "content": "Say hello in Russian"}
	]
)

print(response.choices[0].message.content)