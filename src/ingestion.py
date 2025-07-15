# import os

# # Function to read IP addresses from sample_of_logs.txt and return them as a list
# def load_ip_addresses(file_path):
    
#     ip_list = []

#     if os.path.exists(file_path):
#         with open(file_path, "r") as file:
#             for line in file:
#                 line = line.strip()
#                 if line != "":
#                     ip_list.append(line)
#     else:
#         print(f"File not found: {file_path}")

#     return ip_list

# if __name__ == "__main__":
#     file_path = "data/sample_of_logs.txt"
#     ip_addresses = load_ip_addresses(file_path)

#     print(f"Ingested {len(ip_addresses)} IP addresses:")
#     for ip in ip_addresses:
#         print(ip)


import random

def generate_random_ip():
    """Generate a random IPv4 address."""
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def load_ip_addresses(count=5):
    """Simulate ingesting IPs by generating random ones."""
    ip_list = [generate_random_ip() for _ in range(count)]
    print(f"✅ Ingested {len(ip_list)} random IPs:")
    for ip in ip_list:
        print(ip)
    return ip_list

# Optional manual test
if __name__ == "__main__":
    load_ip_addresses()
