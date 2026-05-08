import json
import os
from datetime import datetime

class IncidentStorage:
    def __init__(self, storage_dir="temp_logs"):
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def log_incident(self, incident_data: dict):
        """
        Saves an incident log locally as a JSON file.
        This ensures data is captured even in Offline Mode.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"incident_{timestamp}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(incident_data, f, indent=4)
        
        print(f"Incident saved locally: {filepath}")
        return filepath

    def get_pending_syncs(self) -> list:
        """Returns all JSON logs that haven't been synced to the cloud yet."""
        return [os.path.join(self.storage_dir, f) for f in os.listdir(self.storage_dir) if f.endswith(".json")]

if __name__ == "__main__":
    storage = IncidentStorage()
    storage.log_incident({"test": "data", "status": "offline_captured"})
