from zk import ZK, const
import sys

def get_device_info(ip, port=4370, password=0):
    zk = ZK(ip, port=port, timeout=5, password=password, force_udp=False, ommit_ping=True)
    conn = None
    try:
        print(f"[*] Connecting to {ip}:{port}...")
        conn = zk.connect()
        print("[+] Connected!")
        
        conn.disable_device()
        
        print("\n" + "="*40)
        print("DEVICE INFORMATION")
        print("-" * 40)
        
        try:
            sn = conn.get_serialnumber()
            print(f"Serial Number: {sn}")
        except Exception as e:
            print(f"Could not get Serial Number: {e}")

        try:
            device_name = conn.get_device_name()
            print(f"Device Name:   {device_name}")
        except Exception as e:
            print(f"Could not get Device Name: {e}")

        try:
            mac = conn.get_mac()
            print(f"MAC Address:   {mac}")
        except Exception as e:
            pass

        try:
            fw = conn.get_firmware_version()
            print(f"Firmware:      {fw}")
        except Exception as e:
            pass

        try:
            platform = conn.get_platform()
            print(f"Platform:      {platform}")
        except Exception as e:
            pass

        print("="*40)
        
        conn.enable_device()
        
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        if conn:
            conn.disconnect()
            print("[*] Disconnected.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        # Default to the one in local_config.py or common default
        ip = "192.168.1.52" 
    
    get_device_info(ip)
