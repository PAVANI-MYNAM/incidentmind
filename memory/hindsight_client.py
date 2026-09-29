import os
import atexit
from dotenv import load_dotenv
from hindsight_client import Hindsight

# Load environment variables from .env
load_dotenv()

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")

HINDSIGHT_BASE_URL = os.getenv(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io"
)

BANK_ID = "incidentmind"

# Check API key
if not HINDSIGHT_API_KEY:
    raise ValueError(
        "HINDSIGHT_API_KEY is missing from the .env file"
    )

# Create Hindsight client
client = Hindsight(
    base_url=HINDSIGHT_BASE_URL,
    api_key=HINDSIGHT_API_KEY
)
# Close the HTTP client cleanly when the Python process exits.
atexit.register(client.close)

def create_memory_bank():
    """
    Create the IncidentMind Hindsight memory bank.
    """
    return client.create_bank(
        bank_id=BANK_ID,
        name="IncidentMind"
    )


def remember_incident(incident):
    """
    Store an incident in Hindsight.

    Hindsight expects the content to be a string,
    so we convert the incident dictionary into
    structured text before storing it.
    """

    symptoms = incident.get("symptoms", [])
    logs = incident.get("logs", [])
    resolution = incident.get("resolution", [])

    # Convert lists into readable text
    symptoms_text = ", ".join(symptoms)
    logs_text = ", ".join(logs)
    resolution_text = ", ".join(resolution)

    content = f"""
Incident ID: {incident.get('incident_id')}

Service: {incident.get('service')}

Severity: {incident.get('severity')}

Timestamp: {incident.get('timestamp')}

Symptoms:
{symptoms_text}

Logs:
{logs_text}

Root Cause:
{incident.get('root_cause')}

Resolution:
{resolution_text}

Resolution Time:
{incident.get('resolution_time_minutes')} minutes

Outcome:
{incident.get('outcome')}

Engineer Feedback:
{incident.get('engineer_feedback')}
""".strip()

    return client.retain(
        bank_id=BANK_ID,
        content=content
    )


def recall_similar_incidents(query):
    """
    Search Hindsight for incidents similar
    to the current incident.
    """

    return client.recall(
        bank_id=BANK_ID,
        query=query
    )
def record_incident_outcome(
    incident,
    actual_root_cause,
    actual_resolution,
    outcome,
    engineer_feedback,
    resolution_time_minutes
):
    """
    Store the final outcome of an incident in Hindsight.

    This is the learning step: the agent remembers
    what actually happened and what ultimately worked.
    """

    resolution_text = ", ".join(actual_resolution)

    content = f"""
Incident Outcome:

Incident ID:
{incident.get('incident_id')}

Service:
{incident.get('service')}

Original Symptoms:
{', '.join(incident.get('symptoms', []))}

Actual Root Cause:
{actual_root_cause}

Actual Resolution:
{resolution_text}

Outcome:
{outcome}

Resolution Time:
{resolution_time_minutes} minutes

Engineer Feedback:
{engineer_feedback}

Learning:
This incident has been resolved. The actual root cause,
successful resolution, outcome, and engineer feedback
should be considered when analyzing similar future incidents.
""".strip()

    return client.retain(
        bank_id=BANK_ID,
        content=content
    )