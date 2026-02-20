# Meraki Network Info Script

This Python script retrieves information from your Cisco Meraki organization and networks. You can fetch **clients** and **devices** data for a chosen network.

---

## Features

- List all organizations and their IDs.
- List all networks in a chosen organization.
- Retrieve clients, devices, or both from a selected network.
- Uses environment variables for your Meraki API token.


## Usage

Install dependencies:

`pip install -r requirements.txt`

Create a .env file with your API token:

token=YOUR_MERAKI_API_TOKEN

Run the script:

python script_name.py

Follow the prompts:

- Enter the path to your .env file.

- Select the organization by copying its ID.

- Select the network by copying its ID.

Choose what information to retrieve:

1 for clients

2 for devices

3 for both

The script will print the results in JSON format.

## Warning

SSL verification is disabled (verify=False) for lab environments.
Do not use in production