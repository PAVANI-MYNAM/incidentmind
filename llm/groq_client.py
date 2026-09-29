import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing from the .env file"
    )

client = Groq(api_key=GROQ_API_KEY)


MODEL = "openai/gpt-oss-120b"


def ask_groq(prompt):
    """
    Send a prompt to Groq and return the AI response.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You are IncidentMind, an AI incident response assistant.

Your job is to help engineers investigate production
incidents using current incident information and
historical incident memory.

Always:
1. Analyze the current symptoms.
2. Use historical incidents as evidence when relevant.
3. Identify the most likely root cause.
4. Explain why the historical incidents are relevant.
5. Recommend a remediation action.
6. Never claim that an action was executed unless the
   system actually executed it.
7. If the evidence is insufficient, clearly say so.
8. Prefer safe, reversible actions.
""",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content