from zk import ZK, const
import sys

def test_zk_connection(ip, port=4370, password=0):
    zk = ZK(ip, port=port, timeout=5, password=password, force_udp=False)
    conn = None
    try:
        print(f"[*] Attemping to connect to ZKTeco device at {ip}:{port} with password {password}...")
        conn = zk.connect()
        print("[+] Connection Successful!")
        
        # Disable device while reading
        conn.disable_device()
        
        # In pyzk, we usually get serial and name directly from the connection object or specific methods
        print("\n" + "="*50)
        try:
            sn = conn.get_sn() # Try get_sn() instead of get_serial_number()
            print(f"Serial Number:  {sn}")
        except:
            pass

        try:
            users = conn.get_users()
            print(f"Users Enrolled: {len(users)}")
        except Exception as ue:
            print(f"Could not fetch users: {ue}")

        print("="*50)
        
        # Re-enable device
        conn.enable_device()
        
    except Exception as e:
        print(f"[!] Connection failed: {e}")
    finally:
        if conn:
            conn.disconnect()
            print("[*] Disconnected from device.")

if __name__ == "__main__":
    # Based on our previous scan
    DEVICE_IP = "192.168.1.31"
    DEVICE_PORT = 4370
    DEVICE_PASSWORD = 0
    
    test_zk_connection(DEVICE_IP, DEVICE_PORT, DEVICE_PASSWORD)
