# ZK Biometric Discovery Tool

A professional utility for automatically discovering and identifying ZKTeco biometric devices within a local network environment. This tool simplifies the setup phase by automating device scanning and metadata retrieval.

## Features
- **Auto-Discovery Suite**: Unified interface for automatic network scanning and device identification
- **Targeted Scanning**: Automatically scans `192.168.1.x` and `192.168.0.x` subnets for active ZK devices
- **Device Management**: Save, test, and manage multiple discovered device configurations
- **Config Export**: Export device settings to `config.env` for use with other attendance scripts
- **Identity Retrieval**: Securely connects to discovered devices to pull unique identifiers (Serial Number, Device Name)
- **Communication Validation**: Built-in verification scripts to ensure network routing and protocol compatibility

## Prerequisites
- Python 3.x
- `pyzk` library

## Installation
```bash
# Install required dependencies
pip install -r requirements.txt
```

## Quick Start

### 🚀 Interactive Device Manager (Recommended)
The easiest way to discover and manage your devices:
```bash
./run_device_manager.sh
```

**Workflow:**
1. Run discovery to find devices on your network (`192.168.1.x` and `192.168.0.x`)
2. Save discovered devices to your local list
3. Export the desired device to `config.env` to make it "Active"
4. Use attendance scripts to fetch data

### 🛠️ Individual Scripts

1. **Standalone Network Scan**:
   ```bash
   python3 scan_network.py
   ```

2. **Fetch Device Identity**:
   ```bash
   python3 get_device_info.py [IP_ADDRESS]
   ```

3. **Verify Handshake**:
   ```bash
   python3 test_connection.py
   ```

4. **Fetch Attendance**:
   ```bash
   python3 fetch_attendance.py --ip [IP] --yesterday
   ```

## Architecture
- `device_manager.py`: Main interactive auto-discovery and management tool
- `scan_network.py`: Implements network sweeping for device discovery
- `get_device_info.py`: Handles session-based connection for info extraction
- `fetch_attendance.py`: Comprehensive attendance data retrieval engine
- `devices.json`: Saved device configurations (auto-generated)
- `config.env`: Active device configuration for automated scripts

---
*Note: This tool is intended for hardware provisioning and discovery.*
