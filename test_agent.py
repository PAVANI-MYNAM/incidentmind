from agent.agent import analyze_incident


test_incident = {
    "incident_id": "INC-LIVE-001",
    "service": "payment-api",
    "severity": "critical",
    "timestamp": "2026-09-28T12:00:00",

    "symptoms": [
        "HTTP 503 errors",
        "database connection timeouts",
        "high payment failure rate"
    ],

    "logs": [
        "DB connection pool exhausted",
        "connection timeout after 30 seconds"
    ]
}


print("=" * 80)
print("INCIDENTMIND")
print("AI INCIDENT RESPONSE AGENT")
print("=" * 80)

print("\nAnalyzing incident...")
print("→ Searching Hindsight memory...")
print("→ Sending historical context to Groq...")
print("→ Generating diagnosis...\n")


try:

    result = analyze_incident(test_incident)

    print("\n")
    print("=" * 80)
    print("HINDSIGHT MEMORIES")
    print("=" * 80)

    for i, memory in enumerate(result["memories"], 1):

        print(f"\nMemory {i}")
        print("-" * 80)
        print(memory)


    print("\n")
    print("=" * 80)
    print("INCIDENTMIND ANALYSIS")
    print("=" * 80)

    print(result["analysis"])


except Exception as e:

    print("\nERROR:")
    print(type(e).__name__, e)