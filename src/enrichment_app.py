import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="config/.env")

MOCK_MODE = os.getenv("MOCK_MODE", "True").lower() == "true"

def enrich_ip(ip):
    """
    Mock enrichment for IP geolocation.
    Returns static data for demo purposes.
    """
    if MOCK_MODE:
        print(f"MOCK_MODE enabled. Returning fake data for {ip}")
        return {
            "ip": ip,
            "city": "London",
            "region": "England",
            "country": "United Kingdom",
            "latitude": 51.5074,
            "longitude": -0.1278
        }
    else:
        print("MOCK_MODE disabled. No real API call implemented in enrichment_app.py.")
        return None

# Manual test
if __name__ == "__main__":
    print(enrich_ip("8.8.8.8"))
