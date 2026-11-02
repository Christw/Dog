
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

SYSTEM_PROMPT = """
You are a helpful AI assistant specializing in dogs.

Answer questions about:
- Dog breeds
- Health
- Nutrition
- Behaviour
- Training
- Grooming and care

Give practical and clear answers.
Do not diagnose medical conditions.
Recommend a veterinarian for serious symptoms or emergencies.
"""

def get_answer(messages):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *messages
        ],
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content
