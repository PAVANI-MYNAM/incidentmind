from memory.hindsight_client import (
    create_memory_bank,
    remember_incident,
    recall_similar_incidents,
    record_incident_outcome
)


print("=" * 70)
print("INCIDENTMIND - HINDSIGHT MEMORY TEST")
print("=" * 70)


try:

    # ============================================================
    # 1. CREATE MEMORY BANK
    # ============================================================

    print("\nCreating IncidentMind memory bank...")

    bank = create_memory_bank()

    print("Memory bank created successfully!")


    # ============================================================
    # 2. STORE INCIDENT
    # ============================================================

    test_incident = {
        "incident_id": "INC-TEST-001",

        "service": "payment-api",

        "severity": "critical",

        "timestamp": "2026-09-28",

        "symptoms": [
            "HTTP 503 errors",
            "database connection timeouts"
        ],

        "logs": [
            "DB connection pool exhausted",
            "connection timeout after 30 seconds"
        ],

        "root_cause": (
            "Database connection pool exhaustion"
        ),

        "resolution": [
            "Increase database connection pool size",
            "Restart payment-api instances"
        ],

        "resolution_time_minutes": 14,

        "outcome": "successful",

        "engineer_feedback": (
            "Increasing the DB pool fixed the issue"
        )
    }


    print("\n" + "=" * 70)
    print("STORING TEST INCIDENT")
    print("=" * 70)

    remember_incident(test_incident)

    print("\nIncident stored successfully!")


    # ============================================================
    # 3. RECALL SIMILAR INCIDENTS
    # ============================================================

    print("\n" + "=" * 70)
    print("SEARCHING HINDSIGHT MEMORY")
    print("=" * 70)

    query = """
    A payment API is returning HTTP 503 errors.

    Database connections are timing out.
    The database connection pool appears exhausted.

    Have we seen a similar incident before?

    What was the root cause and how was it resolved?
    """

    result = recall_similar_incidents(query)

    print("\nRelevant memories:\n")

    for i, memory in enumerate(result.results, 1):

        print("-" * 70)
        print(f"Memory {i}")
        print("-" * 70)
        print(memory.text)


    # ============================================================
    # 4. RECORD FINAL INCIDENT OUTCOME
    # ============================================================

    print("\n" + "=" * 70)
    print("RECORDING INCIDENT OUTCOME")
    print("=" * 70)

    record_incident_outcome(
        incident=test_incident,

        actual_root_cause=(
            "Database connection pool exhaustion "
            "caused by increased concurrent database usage."
        ),

        actual_resolution=[
            "Increased database connection pool size",
            "Restarted payment-api instances"
        ],

        outcome="successful",

        engineer_feedback=(
            "Increasing the connection pool resolved "
            "the 503 errors and payment failures."
        ),

        resolution_time_minutes=12
    )

    print("\nIncident outcome successfully stored!")

    print(
        "IncidentMind has learned from this incident."
    )


    # ============================================================
    # 5. SUMMARY
    # ============================================================

    print("\n" + "=" * 70)
    print("HINDSIGHT MEMORY CYCLE COMPLETE")
    print("=" * 70)

    print("""
STORE
  Incident → Hindsight

RECALL
  Hindsight → Similar historical incidents

LEARN
  Resolved incident → Hindsight

IncidentMind can now use this experience
when analyzing future incidents.
""")


except Exception as e:

    print("\n" + "=" * 70)
    print("ERROR")
    print("=" * 70)

    print(type(e).__name__, e)