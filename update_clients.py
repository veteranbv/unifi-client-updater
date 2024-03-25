import os
import csv
import requests
from dotenv import load_dotenv
import urllib3
import logging

# Load environment variables from .env file
load_dotenv()

# UDM SE URL and credentials
udm_url = os.getenv("UDM_URL")
username = os.getenv("UDM_USERNAME")
password = os.getenv("UDM_PASSWORD")
site_name = os.getenv("UDM_SITE")

# CSV file path
csv_file_path = "data/client_list.csv"

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Enable logging for requests library
logging.basicConfig(level=logging.DEBUG)

# Load CSRF token and session cookie from .env
csrf_token = os.getenv("CSRF_TOKEN")
session_cookie = os.getenv("SESSION_COOKIE")

# Set up session with hardcoded cookie
session = requests.Session()
session.cookies.set("TOKEN", session_cookie.split('=')[1], domain=udm_url.split('//')[1], path="/")
session.headers.update({"X-Csrf-Token": csrf_token})

# Retrieve existing client list
client_list_url = f"{udm_url}/proxy/network/api/s/{site_name}/stat/sta"
response = session.get(client_list_url, verify=False)
response.raise_for_status()
existing_clients = response.json()["data"]

# Read client data from CSV file
with open(csv_file_path, "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        mac_address = row["mac_address"]
        name = row["name"]
        fixed_ip = row.get("fixed_ip")  # Optional fixed IP address

        # Check if client exists
        client = next((c for c in existing_clients if c["mac"] == mac_address), None)

        if client:
            # Update existing client
            update_url = f"{udm_url}/proxy/network/api/s/{site_name}/rest/user/{client['_id']}"
            update_data = {
                "name": name,
                "use_fixedip": bool(fixed_ip),
                "fixed_ip": fixed_ip if fixed_ip else ""
            }
            response = session.put(update_url, json=update_data, verify=False)
            response.raise_for_status()
        else:
            # Create new client
            create_url = f"{udm_url}/proxy/network/api/s/{site_name}/rest/user"
            create_data = {
                "mac": mac_address,
                "name": name,
                "use_fixedip": bool(fixed_ip),
                "fixed_ip": fixed_ip if fixed_ip else "",
                "local_dns_record_enabled": False
            }
            response = session.post(create_url, json=create_data, verify=False)
            response.raise_for_status()