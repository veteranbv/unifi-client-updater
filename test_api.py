import os
import requests
from dotenv import load_dotenv
import urllib3
import logging
import random

# Load environment variables from .env file
load_dotenv()

# UDM SE URL and site name
udm_url = os.getenv("UDM_URL")
site_name = os.getenv("UDM_SITE")

# Load CSRF token and session cookie from .env
csrf_token = os.getenv("CSRF_TOKEN")
session_cookie = os.getenv("SESSION_COOKIE")

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Enable logging for requests library
logging.basicConfig(level=logging.DEBUG)

# Set up session with hardcoded cookie
session = requests.Session()
session.cookies.set("TOKEN", session_cookie.split('=')[1], domain=udm_url.split('//')[1], path="/")
session.headers.update({"X-Csrf-Token": csrf_token})

def generate_random_mac():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

# Test UDM SE connectivity
print("Testing UDM SE connectivity...")
try:
    response = session.get(udm_url, verify=False)
    response.raise_for_status()
    print("UDM SE is reachable.")
except requests.exceptions.RequestException as e:
    print("Error: Failed to connect to UDM SE.")
    print(str(e))
    exit(1)

# Test API endpoints
print("Testing API endpoints...")

# Test /proxy/network/api/s/{site_name}/self endpoint
self_url = f"{udm_url}/proxy/network/api/s/{site_name}/self"
response = session.get(self_url, verify=False)
if response.status_code == 200:
    print("/self endpoint is accessible.")
else:
    print("/self endpoint test failed.")
    print("Status Code:", response.status_code)
    print("Response:", response.text)

# Test /proxy/network/api/s/{site_name}/stat/sta endpoint
sta_url = f"{udm_url}/proxy/network/api/s/{site_name}/stat/sta"
response = session.get(sta_url, verify=False)
if response.status_code == 200:
    print("/stat/sta endpoint is accessible.")
else:
    print("/stat/sta endpoint test failed.")
    print("Status Code:", response.status_code)
    print("Response:", response.text)

# Test /proxy/network/api/s/{site_name}/rest/user endpoint (create/update user)
user_url = f"{udm_url}/proxy/network/api/s/{site_name}/rest/user"
random_mac = generate_random_mac()
test_data = {
    "mac": random_mac,
    "name": "testytest",
    "use_fixedip": False,
    "local_dns_record_enabled": False
}
response = session.post(user_url, json=test_data, verify=False)
if response.status_code == 200:
    print("/rest/user endpoint is accessible.")
else:
    print("/rest/user endpoint test failed.")
    print("Status Code:", response.status_code)
    print("Response:", response.text)

# Clean up test client (if created)
if response.status_code == 200:
    client_mac = test_data["mac"]
    forget_url = f"{udm_url}/proxy/network/api/s/{site_name}/cmd/stamgr"
    forget_data = {
        "cmd": "forget-sta",
        "macs": [client_mac]
    }
    response = session.post(forget_url, json=forget_data, verify=False)
    if response.status_code == 200:
        print(f"Test client {client_mac} successfully forgotten.")
    else:
        print(f"Error forgetting test client {client_mac}: {response.text}")