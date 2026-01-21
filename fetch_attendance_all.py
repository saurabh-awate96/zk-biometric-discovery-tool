#!/usr/bin/env python3
"""
ZKTeco Unified Fetcher - Auto-Discovery & Attendance Retrieval
A single-file solution to discover devices on the network and fetch their attendance data
without manual configuration.
"""

from zk import ZK, const
import sys
import os
import socket
from datetime import datetime, timedelta
import platform
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import requests
import json

class UnifiedBiometricFetcher:
    def __init__(self, port=4370, timeout=1.0, password=0):
        self.port = port
        self.timeout = timeout
        self.password = password
        self.found_devices = []
        self.print_lock = threading.Lock()
        self.config = self.load_full_config()
        self.session = requests.Session()
        if self.config.get('API_KEY') and self.config.get('API_SECRET'):
            self.session.headers.update({
                "Authorization": f"token {self.config['API_KEY']}:{self.config['API_SECRET']}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            })

    def get_local_subnets(self):
        """Attempts to detect local subnets beyond the default ones"""
        subnets = ["192.168.1", "192.168.0"]
        try:
            # Get local IP to guess the subnet
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            
            my_subnet = ".".join(local_ip.split(".")[:-1])
            if my_subnet not in subnets:
                subnets.append(my_subnet)
        except:
            pass
        return subnets

    def check_port(self, ip, port):
        """Checks if a port is open with a more generous timeout"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.5) # Increased for higher reliability on busy networks
                return s.connect_ex((ip, port)) == 0
        except:
            return False

    def load_full_config(self):
        """Loads all configuration from config.env"""
        config = {
            'DEVICE_IP': None,
            'FRAPPE_SITE': None,
            'API_KEY': None,
            'API_SECRET': None,
            'USER_MAP': {}
        }
        try:
            env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.env")
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            key, val = line.split("=", 1)
                            key = key.strip()
                            val = val.strip().strip('"').strip("'")
                            if key == 'USER_MAP':
                                try: config[key] = json.loads(val)
                                except: pass
                            else:
                                config[key] = val
        except Exception as e:
            print(f"[!] Error loading config: {e}")
        return config

    def load_config_ip(self):
        """Backward compatibility for discovery logic"""
        return self.config.get('DEVICE_IP')

    def push_to_frappe(self, att, device_sn, user_name):
        """Pushes a single attendance record to Frappe using the standard HRMS method"""
        site = self.config.get('FRAPPE_SITE')
        api_key = self.config.get('API_KEY')
        api_secret = self.config.get('API_SECRET')
        employee_fieldname = self.config.get('FRAPPE_EMPLOYEE_FIELD', 'attendance_device_id')

        if not site or not api_key or not api_secret:
            return False, "Config Missing (Site/Keys)"

        # Biometric logs usually use 1 for IN, 0 for OUT
        log_type = "IN" if att.status == 1 else "OUT"
        
        # Standard HRMS payload
        payload = {
            "employee_field_value": str(att.user_id),
            "employee_fieldname": employee_fieldname,
            "timestamp": str(att.timestamp),
            "device_id": device_sn,
            "log_type": log_type
        }

        try:
            url = f"{site.rstrip('/')}/api/method/hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field"
            response = self.session.post(url, data=json.dumps(payload), timeout=10)
            
            if response.status_code == 200:
                return True, "Success"
            
            # If rejected, try fallback but log why rejected
            return self.push_to_frappe_fallback(att, device_sn, log_type, f"Method failed ({response.status_code})")
            
        except Exception as e:
            return False, f"Request Error: {str(e)[:20]}"

    def push_to_frappe_fallback(self, att, device_sn, log_type, reason=""):
        """Fallback that looks up Employee first and then inserts Checkin"""
        site = self.config.get('FRAPPE_SITE')
        fieldname = self.config.get('FRAPPE_EMPLOYEE_FIELD', 'attendance_device_id')
        
        try:
            # 1. Lookup employee ID
            url_lookup = f"{site.rstrip('/')}/api/resource/Employee"
            params = {
                "filters": json.dumps([[fieldname, "=", str(att.user_id)]]),
                "fields": json.dumps(["name"])
            }
            res_lookup = self.session.get(url_lookup, params=params, timeout=10)
            
            if res_lookup.status_code != 200:
                return False, f"Lookup HTTP {res_lookup.status_code}"
                
            data = res_lookup.json().get("data", [])
            if not data:
                return False, f"Not Found: {fieldname}={att.user_id}"
            
            employee_id = data[0]["name"]
            
            # 2. Create Checkin
            url_checkin = f"{site.rstrip('/')}/api/resource/Employee Checkin"
            checkin_payload = {
                "employee": employee_id,
                "log_type": log_type,
                "time": str(att.timestamp),
                "device_id": device_sn,
                "plugin_name": "ZK-Biometric-Tool"
            }
            
            res_checkin = self.session.post(url_checkin, data=json.dumps(checkin_payload), timeout=10)
            
            if res_checkin.status_code in [200, 201]:
                return True, "Success (Manual)"
            
            # If manual insert fails, get the error message from Frappe
            err_msg = "Unknown Error"
            try:
                server_msgs = res_checkin.json().get('_server_messages', '[]')
                if isinstance(server_msgs, str):
                    msgs = json.loads(server_msgs)
                    err_msg = msgs[0].get('message', 'No msg') if msgs else "Empty server msgs"
                else:
                    err_msg = f"HTTP {res_checkin.status_code}"
            except:
                err_msg = f"HTTP {res_checkin.status_code}"
                
            return False, f"Push Fail: {err_msg[:20]}"
            
        except Exception as e:
            return False, f"Fallback Exception: {str(e)[:20]}"

    def discover_and_fetch(self, subnets, date_filter):
        """Scans the network and fetches data immediately using concurrency"""
        configured_ip = self.load_config_ip()
        
        # Priority Check: Try configured IP first if it exists
        if configured_ip:
            print(f"[*] Checking priority IP from config: {configured_ip}...")
            if self.check_port(configured_ip, self.port):
                print(f"[+] Priority device found at {configured_ip}")
                if self.fetch_data_from_device(configured_ip, date_filter):
                    return 1, 1 

        print(f"[*] Starting auto-discovery on subnets: {', '.join(subnets)}...")
        print(f"[*] Searching for devices on port {self.port} (Multi-threaded)...")
        
        all_ips = []
        for subnet in subnets:
            for i in range(1, 255):
                all_ips.append(f"{subnet}.{i}")

        found_ips = []
        # Use ThreadPoolExecutor for fast scanning
        max_workers = 100 # Adjust based on system/network capacity
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_ip = {executor.submit(self.check_port, ip, self.port): ip for ip in all_ips}
            
            scanned_count = 0
            for future in as_completed(future_to_ip):
                ip = future_to_ip[future]
                scanned_count += 1
                
                # Feedback every 50 IPs scanned
                if scanned_count % 50 == 0:
                    sys.stdout.write(".")
                    sys.stdout.flush()
                
                try:
                    is_open = future.result()
                    if is_open:
                        found_ips.append(ip)
                        print(f"\n[+] Found active biometric device at {ip}")
                except Exception:
                    pass
        
        print("\n[*] Scan complete.")
        
        if not found_ips:
            return 0, 0

        print(f"[*] Found {len(found_ips)} device(s). Starting data retrieval...")
        
        success_count = 0
        # For fetching data, we can also use threads, but let's do it sequentially or with fewer threads
        # to avoid overwhelming the devices or garbling logs. 
        # Since usually there are few devices, sequential fetching is okay, 
        # but for speed let's use a small pool.
        with ThreadPoolExecutor(max_workers=min(len(found_ips), 5)) as executor:
            future_to_fetch = {executor.submit(self.fetch_data_from_device, ip, date_filter): ip for ip in found_ips}
            for future in as_completed(future_to_fetch):
                if future.result():
                    success_count += 1
            
        return len(found_ips), success_count

    def fetch_data_from_device(self, ip, date_filter=None):
        """Connects to a single device and retrieves all details"""
        zk = ZK(ip, port=self.port, timeout=5, password=self.password, force_udp=False, ommit_ping=True)
        conn = None
        
        output = []
        output.append(f"\n{'='*60}")
        output.append(f"DEVICE PROFILE: {ip}")
        output.append(f"{'='*60}")
        
        try:
            conn = zk.connect()
            conn.disable_device()
            
            # 1. Get Comprehensive Device Info (Same as device_manager.py)
            output.append("[*] Retrieving device information...")
            info = {}
            try: info['SN'] = conn.get_serialnumber()
            except: 
                try: info['SN'] = conn.get_sn()
                except: info['SN'] = "N/A"
            
            try: info['Name'] = conn.get_device_name()
            except: info['Name'] = "N/A"
            
            try: info['Firmware'] = conn.get_firmware_version()
            except: info['Firmware'] = "N/A"
            
            try: info['Platform'] = conn.get_platform()
            except: info['Platform'] = "N/A"
            
            try: info['MAC'] = conn.get_mac()
            except: info['MAC'] = "N/A"
            
            for k, v in info.items():
                output.append(f"    - {k:<10}: {v}")
            
            # 2. Get Users
            output.append("\n[*] Fetching enrolled users...")
            users = conn.get_users()
            output.append(f"    - Total Enrolled: {len(users)}")
            
            # Create a user mapping for better attendance display
            user_map = {u.user_id: u.name for u in users}
            
            # 3. Get Attendance
            label = str(date_filter) if date_filter else "ALL"
            output.append(f"\n[*] Fetching logs for: {label}...")
            attendance = conn.get_attendance()
            
            if date_filter:
                attendance = [att for att in attendance if att.timestamp.date() == date_filter]
            
            output.append(f"    - Records Found: {len(attendance)}")
            
            # Display formatted log & Push to Frappe
            if attendance:
                output.append("\n    " + "-"*75)
                output.append(f"    {'User ID':<10} | {'Name':<25} | {'Timestamp':<25} | {'Status'} | {'Frappe Push'}")
                output.append("    " + "-"*75)
                for att in attendance:
                    u_name = user_map.get(att.user_id, "Unknown")
                    status_label = "Check-Out" if att.status == 0 else "Check-In"
                    
                    # Push feature - ONLY for User 120 during testing
                    push_status = "Skipped (Test Mode)"
                    if str(att.user_id) == "120":
                        success, msg = self.push_to_frappe(att, info['SN'], u_name)
                        push_status = "OK" if success else f"Fail: {msg[:15]}..."
                    
                    output.append(f"    {att.user_id:<10} | {u_name[:25]:<25} | {str(att.timestamp):<25} | {status_label:<8} | {push_status}")
                output.append("    " + "-"*75)
            
            conn.enable_device()
            
            # Thread-safe printing
            with self.print_lock:
                print("\n".join(output))
                
            return True
            
        except Exception as e:
            with self.print_lock:
                print(f"[!] Error processing {ip}: {e}")
            return False
        finally:
            if conn:
                conn.disconnect()

def main():
    parser = argparse.ArgumentParser(description="Unified ZKTeco Auto-Fetch Tool")
    parser.add_argument('--ip', type=str, help='Directly connect to this IP (skips discovery)')
    parser.add_argument('--today', action='store_true', help='Fetch only today\'s attendance')
    parser.add_argument('--yesterday', action='store_true', help='Fetch only yesterday\'s attendance')
    parser.add_argument('--all', action='store_true', help='Fetch all attendance records')
    args = parser.parse_args()

    # Determine date filter - Defaulting to YESTERDAY as requested
    date_filter = None
    if args.today:
        date_filter = datetime.now().date()
        print("[*] Filtering for: TODAY")
    elif args.all:
        date_filter = None
        print("[*] Filtering for: ALL RECORDS")
    else:
        # Default to yesterday
        date_filter = datetime.now().date() - timedelta(days=1)
        print(f"[*] Filtering for: YESTERDAY ({date_filter})")

    fetcher = UnifiedBiometricFetcher()
    
    # 1. Start discovery and immediate fetching
    if args.ip:
        print(f"[*] Using direct IP: {args.ip}")
        total_found = 1
        success_count = 1 if fetcher.fetch_data_from_device(args.ip, date_filter) else 0
    else:
        subnets = fetcher.get_local_subnets()
        total_found, success_count = fetcher.discover_and_fetch(subnets, date_filter)
    
    if total_found == 0:
        print("\n[!] No devices discovered. Ensure you are on the same network as the devices.")
        return

    print(f"\n{'-'*60}")
    print(f"COMPLETE: Processed {success_count} / {total_found} discovered devices.")
    print(f"{'-'*60}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Process cancelled by user.")
        sys.exit(0)
