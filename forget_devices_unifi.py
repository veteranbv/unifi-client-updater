import os
import csv
import requests
from dotenv import load_dotenv

# Load environment variables
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

# CSV file path
csv_file_path = "./data/forget_devices.csv"

# Read MAC addresses from CSV file and forget devices
with open(csv_file_path, "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        mac_address = row["mac_address"]

        # Forget device
        forget_url = f"{controller_url}/proxy/network/api/s/{site_name}/cmd/stamgr"
        forget_data = {"cmd": "forget-sta", "macs": [mac_address]}
        response = session.post(forget_url, json=forget_data, verify=False)

        if response.status_code == 200:
            print(f"Device {mac_address} successfully forgotten.")
        else:
            print(f"Error forgetting device {mac_address}: {response.text}")
