from memory.hindsight_client import recall_similar_incidents
from llm.groq_client import ask_groq


def analyze_incident(incident, use_memory=True):
    """
    Analyze a new incident with or without Hindsight memory.
    """

    symptoms = incident.get("symptoms", [])
    logs = incident.get("logs", [])

    # -------------------------------------------------
    # 1. Build a search query from the current incident
    # -------------------------------------------------

    query = f"""
    Current production incident:

    Service: {incident.get('service')}
    Severity: {incident.get('severity')}

    Symptoms:
    {', '.join(symptoms)}

    Logs:
    {', '.join(logs)}

    Root cause may be unknown.

    Find historical incidents that are similar
    to this incident, especially incidents with
    similar symptoms, service, logs, or failures.
    """

    # -------------------------------------------------
    # 2. Recall historical incidents if memory is enabled
    # -------------------------------------------------

    memories = []

    if use_memory:
        memory_result = recall_similar_incidents(query)

        for memory in memory_result.results:
            memories.append(memory.text)

        # Only use the 4 most relevant memories
        memories = memories[:4]

    historical_memory = "\n\n".join(
        f"Historical Memory {i + 1}:\n{memory}"
        for i, memory in enumerate(memories)
    )

    if not historical_memory:
        historical_memory = """
No historical incident memory is available.

Analyze this incident using only the current
incident symptoms, logs, service, and severity.
"""

    # -------------------------------------------------
    # 3. Build the analysis prompt
    # -------------------------------------------------

    if use_memory:
        memory_instruction = """
Use the historical incidents as organizational evidence.
Compare the current incident with the historical incidents.
Use previous root causes, resolutions, outcomes, and
engineer feedback when they are relevant.

Do not blindly copy a previous resolution.
Clearly distinguish historical evidence from current evidence.
"""
    else:
        memory_instruction = """
Hindsight memory is intentionally disabled.

Analyze ONLY the current incident.
Do not assume knowledge from previous incidents.
Do not invent historical incidents or previous resolutions.
If the available evidence is insufficient, clearly state that.
"""

    prompt = f"""
You are IncidentMind, an AI incident response assistant.

Analyze the current production incident.

{memory_instruction}

========================
CURRENT INCIDENT
========================

Incident ID:
{incident.get('incident_id')}

Service:
{incident.get('service')}

Severity:
{incident.get('severity')}

Timestamp:
{incident.get('timestamp')}

Symptoms:
{', '.join(symptoms)}

Logs:
{', '.join(logs)}

========================
HINDSIGHT MEMORIES
========================

{historical_memory}

========================
YOUR TASK
========================

Provide the response using exactly these sections:

1. Likely Root Cause
2. Evidence From Current Incident
3. Relevant Historical Incidents
4. Recommended Next Steps
5. Confidence

Important rules:

- Do not claim an action was executed.
- Recommendations require engineer approval.
- Clearly distinguish evidence from assumptions.
- If historical memory is disabled, explicitly say that
  no historical memory was used.
- If historical memory is enabled but no relevant memory
  was found, clearly say so.
- Prefer safe and reversible investigation steps.
- Mention specific historical incident IDs when available.
- Provide only 2 to 3 recommended next steps.
- Do not create more than 3 recommendation steps.
"""

    # -------------------------------------------------
    # 4. Ask Groq to analyze the incident
    # -------------------------------------------------

    ai_response = ask_groq(prompt)

    # -------------------------------------------------
    # 5. Return everything needed by the UI
    # -------------------------------------------------

    return {
        "incident": incident,
        "memories": memories[:4],
        "analysis": ai_response,
        "memory_enabled": use_memory,
    }