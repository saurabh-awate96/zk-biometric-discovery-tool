import socket
import sys

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def check_port(ip, port, timeout=0.5):
    """Checks if a specific TCP port is open on an IP address."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            return result == 0
    except Exception:
        return False

def main():
    local_ip = get_local_ip()
    ip_parts = local_ip.split('.')
    network_prefix = ".".join(ip_parts[:3])
    
    # ZKTeco default port
    ZK_PORT = 4370
    
    print(f"[*] Scanning {network_prefix}.0/24 for ZKTeco devices on port {ZK_PORT}...")
    print("[*] Using socket-based scan (no root required)...")
    
    found_devices = []
    
    # Simple loop to scan all IPs in the subnet
    for i in range(1, 255):
        target_ip = f"{network_prefix}.{i}"
        if check_port(target_ip, ZK_PORT):
            print(f"[+] Found device at {target_ip}")
            found_devices.append(target_ip)
        
    print("\n" + "="*50)
    print(f"{'Detected ZKTeco Device IP':<25} | {'Port'}")
    print("-" * 50)
    
    if not found_devices:
        print(f"No devices found on port {ZK_PORT}.")
    else:
        for ip in found_devices:
            print(f"{ip:<25} | {ZK_PORT}")
    
    print("="*50)
    print(f"[*] Scan complete. Found {len(found_devices)} device(s).")

if __name__ == "__main__":
    main()
