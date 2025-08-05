# import requests
# import os
# from dotenv import load_dotenv
# from ingestion import load_ip_addresses

# # Load .env file to get API key
# load_dotenv(dotenv_path="config/.env")
# API_KEY = os.getenv("GEO_IP_API_KEY")

# # Function to enrich a single IP address
# def enrich_ip(ip):
#     url = f"http://api.ipstack.com/{ip}?access_key={API_KEY}"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             return {
#                 "ip": ip,
#                 "city": data.get("city"),
#                 "region": data.get("region_name"),
#                 "country": data.get("country_name"),
#                 "latitude": data.get("latitude"),
#                 "longitude": data.get("longitude")
#             }
#         else:
#             print(f"Error: Status {response.status_code} for IP {ip}")
#             return None
#     except Exception as e:
#         print(f"Exception occurred for IP {ip}: {e}")
#         return None

# # Run enrichment on all IPs
# if __name__ == "__main__":
#     file_path = "data/sample_of_logs.txt"
#     ip_list = load_ip_addresses(file_path)

#     enriched_data = []

#     for ip in ip_list:
#         result = enrich_ip(ip)
#         if result:
#             enriched_data.append(result)

#     # Print results
#     print("\nEnriched Data:")
#     for entry in enriched_data:
#         print(entry)


# import requests
# import os
# from dotenv import load_dotenv
# from ingestion import load_ip_addresses
# from storage import connect_db, create_table, insert_data

# # Load environment variables (for IPStack API and Database)
# load_dotenv(dotenv_path="config/.env")

# API_KEY = os.getenv("GEO_IP_API_KEY")

# # Function to enrich one IP using IPStack
# def enrich_ip(ip):
#     url = f"http://api.ipstack.com/{ip}?access_key={API_KEY}"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             return {
#                 "ip": ip,
#                 "city": data.get("city"),
#                 "region": data.get("region_name"),
#                 "country": data.get("country_name"),
#                 "latitude": data.get("latitude"),
#                 "longitude": data.get("longitude")
#             }
#         else:
#             print(f"Error for IP {ip}: status code {response.status_code}")
#             return None
#     except Exception as e:
#         print(f"Exception for IP {ip}: {e}")
#         return None

# # Run pipeline
# if __name__ == "__main__":
#     # Ingest raw IPs
#     ip_list = load_ip_addresses("data/sample_of_logs.txt")

#     # Enrich each IP
#     enriched_data = []
#     for ip in ip_list:
#         enriched = enrich_ip(ip)
#         if enriched:
#             enriched_data.append(enriched)

#     print(f"\nEnriched {len(enriched_data)} IPs.")

#     # Store in PostgreSQL
#     conn = connect_db()
#     if conn:
#         create_table(conn)
#         insert_data(conn, enriched_data)
#         print("Data successfully stored in PostgreSQL.")
#         conn.close()

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="config/.env")

API_KEY = os.getenv("GEO_IP_API_KEY")

# Function to enrich one IP using IPStack API
def enrich_ip(ip):
    if not API_KEY:
        print("❌ API Key not found. Please set GEO_IP_API_KEY in config/.env")
        return None

    url = f"http://api.ipstack.com/{ip}?access_key={API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()

            # Validate if response contains location data
            if "latitude" in data and "longitude" in data:
                return {
                    "ip": ip,
                    "city": data.get("city"),
                    "region": data.get("region_name"),
                    "country": data.get("country_name"),
                    "latitude": data.get("latitude"),
                    "longitude": data.get("longitude")
                }
            else:
                print(f"⚠️ No location data for IP: {ip}")
                return None
        else:
            print(f"⚠️ API error for IP {ip}: HTTP {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Network/API error for IP {ip}: {e}")
        return None


# Optional manual test
if __name__ == "__main__":
    test_ip = "8.8.8.8"
    print(f"Testing enrichment for IP: {test_ip}")
    print(enrich_ip(test_ip))
