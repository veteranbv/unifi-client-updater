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

# API endpoint for UniFi devices
devices_url = f"{controller_url}/proxy/network/v2/api/site/{site_name}/device"

# Query parameters
params = {
    "separateUnmanaged": "true",
    "includeTrafficUsage": "true"
}

# Send GET request to retrieve UniFi devices
response = session.get(devices_url, params=params, verify=False)
response.raise_for_status()

# Extract device data from the response
devices_data = response.json()

# CSV file path
csv_file_path = "data/unifi_devices.csv"

# Flatten the nested device data
flattened_devices = []
for device in devices_data["network_devices"]:
    flattened_device = {}
    for key, value in device.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                flattened_device[f"{key}.{sub_key}"] = sub_value
        else:
            flattened_device[key] = value
    flattened_devices.append(flattened_device)

# Get the union of all keys from all dictionaries in flattened_devices
fieldnames = set()
for device in flattened_devices:
    fieldnames.update(device.keys())

# Specify the order of the common fields
common_fields = ["mac", "name", "model", "type", "version", "ip"]

# Remove the common fields from fieldnames
fieldnames = fieldnames - set(common_fields)

# Sort the remaining fields alphabetically
sorted_fields = sorted(fieldnames)

# Combine the common fields and sorted fields
final_fieldnames = common_fields + sorted_fields

# Write device data to CSV file
with open(csv_file_path, "w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=final_fieldnames)
    writer.writeheader()
    writer.writerows(flattened_devices)

print(f"UniFi devices data saved to {csv_file_path}")