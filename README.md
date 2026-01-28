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
To support multiple devices or machines running simultaneously, map Serial Numbers or Device IDs (Machine Number) to Shift Types:
```bash
# JSON format: {"Shift Name": ["IDENTIFIER1", "IDENTIFIER2"]}
SHIFT_DEVICE_MAP='{"General Shift": ["SN123456789", "1"], "Night Shift": ["SN987654321"]}'
```

---

## ⏰ Automation (Running every 30 mins)

To keep your attendance data synced automatically, you can set up a scheduled task.

### 🐧 Linux & 🍎 macOS (using `cron` + `flock`)

1. **Find your Python path**:
   ```bash
   which python3
   ```
2. **Open crontab**:
   ```bash
   crontab -e
   ```
3. **Add the following line** (Replace `/path/to/tool` with your actual directory):
   ```bash
   */30 * * * * flock -n /tmp/zk_biometric.lock -c "cd /path/to/tool && /usr/bin/python3 fetch_attendance_all.py >> cron_log.txt 2>&1"
   ```
   > [!TIP]
   > `flock -n` ensures that if a previous sync is still running, a new one won't start, preventing duplicate processes.

---

### 🪟 Windows (using Task Scheduler)

1. **Set up Task Scheduler**:
   - Open **Task Scheduler** and click **Create Basic Task**.
   - Name: `ZK_Biometric_Sync`.
   - Trigger: **Daily** -> set any start time -> click Next.
   - Action: **Start a program** -> Browse and select the `run_sync.bat` file in the tool folder.
   - Click **Finish**.

2. **Configure Repeat Interval**:
   - Right-click the new task -> **Properties**.
   - **Triggers** tab -> Select the trigger -> **Edit**.
   - Check **Repeat task every:** and set to `30 minutes`.
   - Set **for a duration of:** to `Indefinitely`.
3. **Ensure Process Safety**:
   - Go to the **Settings** tab.
   - Under "If the task is already running...", select **Do not start a new instance**.

---

## ❓ Troubleshooting

- **No devices discovered**: Ensure your computer is on the same local network as the devices.
- **Connection Timeout**: The device might be busy or the network is unstable. Try running the command again.
- **Multi-Machine Sync**: If running from multiple locations, ensure each machine manages different devices/shifts via `SHIFT_DEVICE_MAP`.
- **Duplicate Processes**: On Linux/macOS, `flock` handles this. On Windows, ensure the Task Scheduler "Do not start a new instance" setting is checked.

---
*Note: This tool is intended for hardware provisioning and discovery.*
