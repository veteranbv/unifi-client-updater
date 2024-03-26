import os
import csv
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# UniFi Controller settings
controller_url = os.getenv("UDM_URL")
site_name = os.getenv("UDM_SITE")

# Load CSRF token and session cookie from .env
csrf_token = os.getenv("CSRF_TOKEN")
session_cookie = os.getenv("SESSION_COOKIE")

# Set up session with hardcoded cookie
session = requests.Session()
session.cookies.set("TOKEN", session_cookie.split('=')[1], domain=controller_url.split('//')[1], path="/")
session.headers.update({"X-Csrf-Token": csrf_token})

# API endpoint for active clients
clients_url = f"{controller_url}/proxy/network/v2/api/site/{site_name}/clients/active"

# Query parameters
params = {
    "includeTrafficUsage": "true",
    "includeUnifiDevices": "true"
}

# Send GET request to retrieve active clients
response = session.get(clients_url, params=params, verify=False)
response.raise_for_status()

# Extract client data from the response
clients_data = response.json()

# CSV file path
csv_file_path = "data/active_clients.csv"

# Get the union of all keys from all dictionaries in clients_data
fieldnames = set()
for client in clients_data:
    fieldnames.update(client.keys())

# Specify the order of the common fields - these will be the first columns in the CSV
common_fields = ["mac", "name", "fixed_ip", "use_fixedip", "ip"]

# Remove the common fields from fieldnames
fieldnames = fieldnames - set(common_fields)

# Sort the remaining fields alphabetically
sorted_fields = sorted(fieldnames)

# Combine the common fields and sorted fields. Remove sorted fields from this if you only want the common fields.
final_fieldnames = common_fields + sorted_fields

# Write client data to CSV file
with open(csv_file_path, "w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=final_fieldnames)
    writer.writeheader()
    writer.writerows(clients_data)

print(f"Active clients data saved to {csv_file_path}")