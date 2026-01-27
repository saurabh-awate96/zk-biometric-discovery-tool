# ZK Biometric Discovery Tool

A professional utility for automatically discovering and identifying ZKTeco biometric devices within a local network. It handles discovery, identity retrieval, and attendance fetching in one pass.

##  Features
- **Auto-Discovery**: Automatic network scanning and device identification.
- **Multi-OS Support**: Optimized for Windows, Linux, and macOS.
- **ERP Integration**: Pushes attendance logs to Frappe/ERPNext.
- **Advanced Syncing**: Supports mapping specific devices to individual Shift Types for independent synchronization.

## 💻 OS-Specific Setup & Usage

Select your operating system below for tailored instructions.

---

### 🪟 Windows (Command Prompt / PowerShell)

1.  **Prerequisites**:
    - Python 3.7+ installed.
    - Network access to biometric devices (Wi-Fi or LAN).
2.  **Download/Clone**: Extract the project to a folder (e.g., `C:\zk-tool`).
3.  **Open Terminal**: Open **Command Prompt** or **PowerShell**.
4.  **Navigate**: `cd C:\zk-tool`
5.  **Install Dependencies**:
    ```cmd
    pip install -r requirements.txt
    ```
6.  **Run the Tool**:
    ```cmd
    # Discover devices and view logs
    python fetch_attendance_all.py
    ```

---

### 🐧 Linux (Ubuntu/Debian)

1.  **Prerequisites**:
    - Network access to biometric devices (Wi-Fi or LAN).
2.  **Install Python & Pip**:
    ```bash
    sudo apt update && sudo apt install python3 python3-pip
    ```
3.  **Navigate to Project**: `cd path/to/zk-biometric-discovery-tool`
4.  **Install Dependencies**:
    ```bash
    pip3 install -r requirements.txt
    ```
5.  **Run the Tool**:
    ```bash
    # Discover devices and view logs
    python3 fetch_attendance_all.py
    ```

---

### 🍎 macOS

1.  **Prerequisites**:
    - Network access to biometric devices (Wi-Fi or LAN).
2.  **Automated Setup**:
    ```bash
    chmod +x setup_mac.sh && ./setup_mac.sh
    ```
3.  **Manual Setup** (if automated fails):
    - Install [Homebrew](https://brew.sh/).
    - `brew install python`
    - `pip3 install -r requirements.txt`
4.  **Run the Tool**:
    ```bash
    # Discover devices and view logs
    python3 fetch_attendance_all.py
    ```

---

## ⚙️ Configuration (`config.env`)

Before running the tool in production mode, edit `config.env` to connect to your ERP and configure device mappings.

### Basic ERP Config
- `FRAPPE_SITE`: Your ERP URL (e.g., `https://your-erp.com`).
- `API_KEY` & `API_SECRET`: Your User API keys.

### Advanced Shift-Device Mapping
To support multiple devices or machines running simultaneously, map Serial Numbers to Shift Types:
```bash
# JSON format: {"Shift Name": ["DEVICESERIALNUMBER"]}
SHIFT_DEVICE_MAP='{"General Shift": ["SN123456789"], "Night Shift": ["SN987654321"]}'
```

---

## ❓ Troubleshooting

- **No devices discovered**: Ensure your computer is on the same local network as the devices.
- **Connection Timeout**: The device might be busy or the network is unstable. Try running the command again.
- **Multi-Machine Sync**: If running from multiple locations, ensure each machine manages different devices/shifts via `SHIFT_DEVICE_MAP`.

---
*Note: This tool is intended for hardware provisioning and discovery.*
