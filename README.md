# ZK Biometric Discovery Tool

A professional utility for automatically discovering and identifying ZKTeco biometric devices within a local network environment. This tool simplifies the setup phase by automating device scanning and metadata retrieval.

## 🚀 Unified Auto-Discovery
The tool is now unified into a single, powerful script: `fetch_attendance_all.py`. It handles discovery, identity retrieval, and attendance fetching in one pass.

## 📋 Features
- **Auto-Discovery**: Unified interface for automatic network scanning and device identification.
- **Multi-OS Support**: Optimized for Windows, Linux, and macOS.
- **Identity Retrieval**: Securely connects to discovered devices to pull Serial Numbers, MAC addresses, and more.
- **ERP Integration**: Built-in support for pushing attendance logs to Frappe/ERPNext.

## 🛠️ Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/saurabh-awate96/zk-biometric-discovery-tool.git
cd zk-biometric-discovery-tool

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Tool
```bash
# Simple discovery and attendance view (Recommended)
python3 fetch_attendance_all.py --no-push
```

## 📖 OS-Specific Guides
For detailed setup instructions on your specific operating system, please see the standalone guide:
👉 **[Standalone Setup Guide (Windows, Linux, macOS)](README_STANDALONE.md)**

## 📂 Architecture
- `fetch_attendance_all.py`: The main unified script for discovery and retrieval.
- `setup_mac.sh`: Automated environment setup for macOS users.
- `config.env`: Centralized configuration for device ports and ERP credentials.
- `requirements.txt`: Python package dependencies.

---
*Note: This tool is intended for hardware provisioning and discovery.*
