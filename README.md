# ZK Biometric Discovery Tool

A professional utility for discovering and identifying ZKTeco biometric devices within a local network environment. This tool is designed to simplify the initial setup phase by automating device scanning and metadata retrieval.

## Features
- **Network Discovery**: Multi-threaded scanning of local subnets to identify active ZK devices.
- **Identity Retrieval**: Securely connects to discovered devices to pull unique identifiers (Serial Number, Device Name).
- **Communication Validation**: Built-in verification scripts to ensure network routing and protocol compatibility.

## Prerequisites
- Python 3.x
- `pyzk` library

## Installation
```bash
# Install required dependencies
pip install -r requirements.txt
```

## Quick Start
1. **Discover Devices**: Find all ZKTeco devices on your current subnet.
   ```bash
   python scan_network.py
   ```
2. **Fetch Identity**: Retrieve the serial number and firmware name for a specific device.
   ```bash
   python get_device_info.py
   ```
3. **Verify Connection**: Test basic packet exchange with a known IP.
   ```bash
   python test_connection.py
   ```

## Architecture
- `scan_network.py`: Implements UDP/TCP sweeping for device discovery.
- `get_device_info.py`: Handles session-based connection to ZK protocol for info extraction.
- `test_connection.py`: Simple handshake validation.

---
*Note: This tool is intended for initial hardware provisioning and discovery.*
