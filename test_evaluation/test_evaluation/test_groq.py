from llm.groq_client import ask_groq


prompt = """
A payment API is returning HTTP 503 errors.

Symptoms:
- Database connection timeouts
- High payment failure rate
- Database connection pool appears exhausted

Historical evidence:
A previous incident had the same symptoms.
Its root cause was database connection pool exhaustion.
The issue was resolved by increasing the database
connection pool size and restarting payment-api instances.

Analyze the current incident and recommend what the
engineer should do.
"""


print("Asking IncidentMind AI...\n")

try:
    response = ask_groq(prompt)

    print("AI RESPONSE:")
    print("=" * 70)
    print(response)

except Exception as e:
    print("\nERROR:")
    print(type(e).__name__, e)