# UniFi Client Manager

UniFi Client Manager is a Python project that provides a set of scripts to automate various tasks related to managing client devices in a UniFi network managed by a UDM SE (UniFi Dream Machine Special Edition) using the UniFi Controller API. The project includes scripts for updating client information, forgetting devices, and testing the API connectivity.

## Features

- Update client names and assign fixed IP addresses based on a CSV file (`update_clients.py`).
- Forget devices based on MAC addresses provided in a CSV file (`forget_devices_unifi.py`).
- Test the connectivity and functionality of the UniFi Controller API endpoints (`test_api.py`).

## Prerequisites

- Python 3.x
- `requests` library
- `python-dotenv` library
- `urllib3` library

## Installation

1. Clone the repository or download the project files.

2. Navigate to the project directory:

    ```bash
    cd unifi-client-manager
    ```
3. Initialize a Python Virtual Environment (Optional):
    ```bash
    python -m venv .
    source ./bin/activate
    ```

    Follow your python distribution or OS-recommended method for installing the `venv` module if not already available, or skip this step.

4. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

5. Create a `.env` file in the project directory and provide the following information:

    ```env
    UDM_URL=https://your-udm-se-url
    UDM_SITE=your-site-name
    CSRF_TOKEN=your-csrf-token
    SESSION_COOKIE=your-session-cookie
    ```

    Replace `your-udm-se-url`, `your-site-name`, `your-csrf-token`, and `your-session-cookie` with the actual values obtained from your UDM SE setup (see below for an example). The cookie and csrf are both easily captured by logging into your UDM and copying the cookie and csrf token from the browser. This will only work for the session time of the cookie.

### Obtaining Cookie/Tokens for `.env` (Google Chrome)
1. Login to the local interface for your UDM/UniFi Network console (not Cloud/Remote Access). 
2. Right Click -> Inspect. 
3. Choose the `Network` tab, refresh the page, then pick a resource that has both of the required values below (`device`, `info`, and a few others work).
4. Within `Headers` sub-tab, copy the string listed within the `Cookie:` header that begins with `TOKEN=` (include this prefix) until the location it ends in a semicolon `;` (not including the semicolon). Paste this value as your `SESSION_COOKIE` in the `.env` file.
5. At the bottom of `Headers`, copy the entire string listed within `X-Csrf-Token:` and paste this value as your `CSRF_TOKEN` value in the `.env` file.
6. `UDM_SITE` refers to the site name within the UniFi Network application running on your console, not the console name. The site name is in the local URL, for example `https://<host_or_ip>/network/<site>/dashboard`. For most installations without a multi-site setup within the Network application this will likely be `default`.

## Usage

### Updating Client Information

1. Prepare a CSV file (`client_list.csv`) with the client information. The CSV file should have the following columns:
    - `mac_address`: The MAC address of the client device.
    - `name`: The desired name for the client device.
    - `fixed_ip` (optional): The fixed IP address to assign to the client device.
    - `local_dns` (optional): The local DNS record to assign to the client device.
    - `note` (optional): The note to assign to the client device.

    Place the CSV file in the `data` directory.

2. Run the `update_clients.py` script:

    ```bash
    python update_clients.py
    ```

    The script will authenticate with the UDM SE, retrieve the existing client list, and update the client information based on the CSV file. If a client doesn't exist, it will be created.

### Forgetting Devices

1. Prepare a CSV file (`forget_devices.csv`) with the MAC addresses of the devices you want to forget. The CSV file should have the following column:
    - `mac_address`: The MAC address of the device to forget.

    Place the CSV file in the `data` directory.

2. Run the `forget_devices_unifi.py` script:

    ```bash
    python forget_devices_unifi.py
    ```

    The script will read the MAC addresses from the CSV file and send requests to the UniFi Controller API to forget the corresponding devices.

### Retrieving Active Clients

1. Run the `get_active_clients.py` script:

    ```bash
    python get_active_clients.py
    ```

    The script will retrieve the active clients from the UniFi Controller API and save the information to a CSV file (`active_clients.csv`) in the `data` directory. You can modify the script to reduce or customize what fields are saved to the CSV file.

### Retrieving Historic Clients

1. Run the `get_historic_clients.py` script:

    ```bash
    python get_historic_clients.py
    ```

    The script will retrieve the historic or currently disconnected clients from the UniFi Controller API and save the information to a CSV file (`historic_clients.csv`) in the `data` directory. You can modify the script to reduce or customize what fields are saved to the CSV file.

### Retrieving UniFi Devices

1. Run the `get_unifi_clients.py` script:

    ```bash
    python get_unifi_clients.py
    ```

    The script will retrieve the list of UniFi devices from the UniFi Controller API and save the information to a CSV file (`unifi_devices.csv`) in the `data` directory. You can modify the script to reduce or customize what fields are saved to the CSV file.

### Testing API Connectivity

1. Run the `test_api.py` script:

    ```bash
    python test_api.py
    ```

    The script will test the connectivity to the UDM SE and various API endpoints, including `/self`, `/stat/sta`, and `/rest/user`. It creates a test client with a randomly generated MAC address, verifies the accessibility of the endpoints, and then cleans up the test client by forgetting it.

## Project Structure

```text
unifi-client-manager/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── forget_devices_unifi.py
├── get_active_clients.py
├── get_historic_clients.py
├── get_unifi_clients.py
├── test_api.py
├── update_clients.py
└── data/
    ├── active_clients.csv
    ├── client_list.csv
    ├── forget_devices.csv
    ├── historic_clients.csv
    └── unifi_devices.csv
```

- `.env`: Contains sensitive information like the UDM SE URL, site name, CSRF token, and session cookie.
- `.gitignore`: Specifies files and directories to be ignored by version control.
- `README.md`: Provides information and instructions for the project.
- `requirements.txt`: Lists the required Python packages.
- `forget_devices_unifi.py`: Script to forget devices based on MAC addresses provided in a CSV file.
- `get_active_clients.py`: Script to retrieve the active clients from the UniFi Controller API.
- `get_historic_clients.py`: Script to retrieve the historic or currently disconnected clients from the UniFi Controller API.
- `test_api.py`: Script to test the connectivity and functionality of the UniFi Controller API endpoints.
- `update_clients.py`: Script to update client information using the UniFi Controller API.
- `data/`: Directory to store the CSV files containing client information and MAC addresses.

## Notes

- The scripts assume you have the necessary permissions to perform these actions on your UDM SE.
- The scripts disable SSL verification to handle self-signed certificates. Adjust the code accordingly based on your specific setup and security requirements.
- The `.env` file and the `data` directory are ignored by version control to prevent sensitive information from being accidentally committed.

## Acknowledgements

Special thanks to the contributors of the unofficial Ubiquiti UniFi Controller API documentation. Their efforts in creating and maintaining the [UniFi Controller API documentation](https://ubntwiki.com/products/software/unifi-controller/api) made this project possible. While I had to update some of the endpoints and methods, their work was invaluable in getting started.
