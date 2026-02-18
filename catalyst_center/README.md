# Cisco Catalyst Center – Running Config Backup

This Python script retrieves the **running configuration** of all devices in a **Cisco Catalyst Center** using the API and saves each config to a text file.

## How it works
1. Authenticates to the Cisco Catalyst Center API.
2. Gets the list of devices.
3. Downloads the running-config for each device.
4. Saves files as:

## Configuration

Create a cred.env file in the same folder as the script:

username=your_username
password=your_password

## Usage

Run the script:

python script.py

Then enter:

- IP address of the Cisco Catalyst Center

- Folder to save the files

## Output

Configurations are saved in the chosen folder:

running_switch1.txt
running_router1.txt
...

## Warning

SSL verification is disabled (verify=False) for lab environments.
Do not use as-is in production