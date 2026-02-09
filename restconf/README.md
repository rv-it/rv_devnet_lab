# RESTCONF Interface and Static Route Automation

This folder contains Python scripts that use **RESTCONF** and **IETF YANG models** to retrieve and configure network interfaces and static routes on Cisco devices.

These scripts are for **lab environments** or **DevNet practice**.

---

## Scripts Overview

### 1. Interface Management Script
**Purpose:**
- Retrieve interface information (GET)
- Configure an IPv4 address on an interface (PATCH)
- Create a Loopback interface if it does not exist

**Main features:**
- Lists all interfaces and their IP configuration
- Supports:
  - `GigabitEthernet`
  - `Loopback`
- Uses the `ietf-interfaces` and `ietf-ip` YANG models

---

### 2. Static Route and VRF Script
**Purpose:**
- Display existing VRF instances
- Create a VRF instance if it does not exist
- Add a static route to a VRF

**Main features:**
- Uses the `ietf-routing` and `ietf-ipv4-unicast-routing` YANG models
- Automatically checks if the VRF exists before creating it


