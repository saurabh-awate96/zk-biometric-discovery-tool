# Standalone Setup Guide - ZK Biometric Discovery Tool

This guide explains how to run the Biometric Discovery Tool on any Windows or Linux machine without requiring a Frappe/ERPNext installation.

## Prerequisites

- **Python 3.7+**: Ensure Python is installed on your system.
  - Windows: [python.org](https://www.python.org/downloads/) (Check "Add Python to PATH" during installation)
  - Linux: `sudo apt install python3 python3-pip`

## Setup Instructions

### 1. Download the Tool
- **Option A (Git)**: Run `git clone https://github.com/saurabh-awate96/zk-biometric-discovery-tool.git`
- **Option B (Zip)**: Download the project as a ZIP from GitHub and extract it to a folder (e.g., `C:\zk-tool`).

### 2. Open Terminal
- **Windows**: Press `Win + R`, type `cmd` or `powershell`, and press Enter.
- **Linux**: Open your favorite terminal emulator.

### 3. Navigate to the Folder
Use the `cd` command to enter the tool's directory:
```bash
# Example for Windows
cd C:\zk-tool
# Example for Linux
cd ~/zk-biometric-discovery-tool
```

### 4. Install Dependencies
```bash
# Windows
pip install -r requirements.txt

# Linux
pip3 install -r requirements.txt
```

## Running the Tool on Windows

Once dependencies are installed, you can scan your network:

1. **Verify Python**: Type `python --version`. It should show 3.7 or higher.
2. **Run Scan**:
   ```cmd
   python fetch_attendance_all.py --no-push
   ```
3. **Target Specific IP** (if discovery is slow):
   ```cmd
   python fetch_attendance_all.py --ip 192.168.1.31 --no-push
   ```

### 3. Configuration (Optional)
If you just want to scan your network and see logs on your screen, you don't need any configuration.

If you eventually want to push data to an ERP, edit `config.env`:
- `DEVICE_PORT`: Default is 4370.
- `FRAPPE_SITE`: Your ERP URL.
- `API_KEY` & `API_SECRET`: Your User API keys.

## Running the Tool

### A. Simple Discovery (Local Only)
To scan the network and display attendance on your screen without trying to connect to any ERP:

```bash
python fetch_attendance_all.py --no-push
```

### B. Fetch for a Specific Date
```bash
# Fetch yesterday's data (Default)
python fetch_attendance_all.py --no-push

# Fetch today's data
python fetch_attendance_all.py --today --no-push

# Fetch all historical data
python fetch_attendance_all.py --all --no-push
```

### C. Connect to a Specific Device IP
If you already know the IP of your biometric device:

```bash
python fetch_attendance_all.py --ip 192.168.1.31 --no-push
```

## Troubleshooting

- **No devices discovered**: Ensure your computer is on the same local network (Wi-Fi or LAN) as the biometric devices.
- **Connection Timeout**: The device might be busy or the network is unstable. Try running the command again.
- **Permission Denied (Linux)**: Some systems may require `sudo` if you are accessing restricted network ports, though usually not required for this tool.
