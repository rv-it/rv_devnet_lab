# NETCONF Interface and User Automation

This folder contains Python scripts that use **NETCONF** and **YANG models** to configure Cisco IOS XE devices.

These scripts are for **lab environments** or **DevNet practice** and have been **tested only** on the **"IOS XE on Cat8kv"** sandbox..

---

## Scripts Overview

### 1. Interface Management Script
**Purpose:**
- Retrieve interface configuration using NETCONF
- Configure an IPv4 address on an interface
- Create a Loopback interface if it does not exist

**Main features:**
- Uses the `ietf-interfaces` and `ietf-ip` YANG models
- Displays all available interfaces
- Allows configuration of:
  - `GigabitEthernet`
  - `Loopback`

**Operations:**
- `get-config` to retrieve interface data
- `edit-config` to apply interface configuration

---

### 2. Local User Creation Script
**Purpose:**
- Create a local user account on a Cisco IOS XE device

**Main features:**
- Prompts for:
  - Username
  - Privilege level
  - Password (hidden input)
- Uses the `Cisco-IOS-XE-native` YANG model
- Applies configuration with NETCONF `edit-config`

