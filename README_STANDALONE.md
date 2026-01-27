# Standalone Setup Guide - ZK Biometric Discovery Tool

This guide explains how to run the Biometric Discovery Tool on any machine without requiring a Frappe/ERPNext installation. The tool is now unified into a single script: `fetch_attendance_all.py`.

---

## 📋 Prerequisites (All Systems)
- **Python 3.7+**: Required to run the script.
- **Network**: Your computer must be on the same local network (Wi-Fi or LAN) as the biometric devices.

---

## 🪟 Windows Setup & Usage

### 1. Installation
- Download the project as a ZIP from GitHub and extract it (e.g., `C:\zk-tool`).
- Open **Command Prompt** or **PowerShell**.
- Navigate to the folder: `cd C:\zk-tool`
- Install dependencies:
  ```cmd
  pip install -r requirements.txt
  ```

### 2. Running the Tool
- **Auto-Discovery (Scan Network)**:
  ```cmd
  python fetch_attendance_all.py --no-push
  ```
- **Fetch Today's Data**:
  ```cmd
  python fetch_attendance_all.py --today --no-push
  ```
- **Target Specific IP**:
  ```cmd
  python fetch_attendance_all.py --ip 192.168.1.31 --no-push
  ```

---

## 🐧 Linux Setup & Usage

### 1. Installation
- Open your terminal.
- Clone the repo or navigate to the folder.
- Install Python & Pip (if not present): `sudo apt install python3 python3-pip`
- Install dependencies:
  ```bash
  pip3 install -r requirements.txt
  ```

### 2. Running the Tool
- **Auto-Discovery (Scan Network)**:
  ```bash
  python3 fetch_attendance_all.py --no-push
  ```
- **Fetch Today's Data**:
  ```bash
  python3 fetch_attendance_all.py --today --no-push
  ```
- **Target Specific IP**:
  ```bash
  python3 fetch_attendance_all.py --ip 192.168.1.31 --no-push
  ```

---

## 🍎 macOS Setup & Usage

### 1. Installation
- Open **Terminal**.
- Install [Homebrew](https://brew.sh/) if you don't have it.
- Use the automated setup script (Recommended):
  ```bash
  chmod +x setup_mac.sh && ./setup_mac.sh
  ```
- *OR Manual install*:
  ```bash
  brew install python
  pip3 install -r requirements.txt
  ```

### 2. Running the Tool
- **Auto-Discovery (Scan Network)**:
  ```bash
  python3 fetch_attendance_all.py --no-push
  ```
- **Fetch Today's Data**:
  ```bash
  python3 fetch_attendance_all.py --today --no-push
  ```
- **Target Specific IP**:
  ```bash
  python3 fetch_attendance_all.py --ip 192.168.1.31 --no-push
  ```

---

## ⚙️ Configuration (Optional)

If you eventually want to push data to an ERP, edit `config.env`:
- `DEVICE_PORT`: Default is 4370.
- `FRAPPE_SITE`: Your ERP URL (e.g., `https://your-erp.com`).
- `API_KEY` & `API_SECRET`: Your User API keys.

---

## ❓ Troubleshooting

- **No devices discovered**: Ensure your computer is on the same local network.
- **Connection Timeout**: The device might be busy or the network is unstable. Try running the command again.
- **Permission Denied (Linux)**: Some systems may require `sudo` for certain network operations.
