import requests
import os
from dotenv import load_dotenv
from ingestion import load_ip_addresses

# Load .env file to get API key
load_dotenv(dotenv_path="config/.env")
API_KEY = os.getenv("GEO_IP_API_KEY")

# Function to enrich a single IP address
def enrich_ip(ip):
    url = f"http://api.ipstack.com/{ip}?access_key={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "ip": ip,
                "city": data.get("city"),
                "region": data.get("region_name"),
                "country": data.get("country_name"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude")
            }
        else:
            print(f"Error: Status {response.status_code} for IP {ip}")
            return None
    except Exception as e:
        print(f"Exception occurred for IP {ip}: {e}")
        return None

# Run enrichment on all IPs
if __name__ == "__main__":
    file_path = "data/sample_of_logs.txt"
    ip_list = load_ip_addresses(file_path)

    enriched_data = []

    for ip in ip_list:
        result = enrich_ip(ip)
        if result:
            enriched_data.append(result)

    # Print results
    print("\nEnriched Data:")
    for entry in enriched_data:
        print(entry)
