#!/bin/bash
# MacOS Setup Script for ZK Biometric Discovery Tool

echo "------------------------------------------------"
echo "  ZK Biometric Discovery Tool - MacOS Setup"
echo "------------------------------------------------"

# 1. Check for Brew
if ! command -v brew &> /dev/null
then
    echo "[!] Homebrew not found. Please install it from https://brew.sh/"
    echo "    Or manually ensure Python 3.7+ is installed."
    exit 1
fi

# 2. Check for Python
echo "[*] Checking for Python 3..."
if ! command -v python3 &> /dev/null
then
    echo "[*] Python 3 not found. Installing via Homebrew..."
    brew install python
else
    echo "[+] Python 3 is already installed."
fi

# 3. Install Dependencies
echo "[*] Installing dependencies from requirements.txt..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# 4. Success
echo ""
echo "------------------------------------------------"
echo "  Setup Complete! You can now run the tool:"
echo "  python3 fetch_attendance_all.py --no-push"
echo "------------------------------------------------"
