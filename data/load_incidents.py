import json
from memory.hindsight_client import remember_incident


def load_incidents():
    with open("data/incidents.json", "r", encoding="utf-8") as file:
        return json.load(file)


def store_all_incidents():
    incidents = load_incidents()

    for incident in incidents:
        print(f"Storing {incident['incident_id']}...")
        remember_incident(incident)

    print(f"\nStored {len(incidents)} incidents in Hindsight.")


if __name__ == "__main__":
    store_all_incidents()