import subprocess
import platform
from typing import List, Dict, Any
import time

def ping_ips(ip_addresses: List[str], timeout: int = 1, count: int = 4) -> Dict[str, Any]:
    """
    Pings a list of IP addresses sequentially and returns the results.
    
    Args:
        ip_addresses: List of IP addresses to ping
        timeout: Timeout in seconds for each ping
        count: Number of pings to send to each address
        
    Returns:
        Dictionary with IP addresses as keys and ping results as values
    """
    results = {}
    
    # Determine the ping command based on the OS
    param = "-n" if platform.system().lower() == "windows" else "-c"
    timeout_param = "-w" if platform.system().lower() == "windows" else "-W"
    
    for ip in ip_addresses:
        command = ["ping", param, str(count), timeout_param, str(timeout), ip]
        
        start_time = time.time()
        try:
            output = subprocess.check_output(command, universal_newlines=True)
            success = True
        except subprocess.CalledProcessError:
            output = "Ping failed"
            success = False
        
        ping_time = time.time() - start_time
        
        results[ip] = {
            "success": success,
            "output": output,
            "time": ping_time
        }
        
        # Print progress
        print(f"Pinged {ip}: {'Success' if success else 'Failed'} (Time: {ping_time:.3f}s)")
    
    return results

# Example usage
if __name__ == "__main__":
    # Example IPs
    ips = ["192.168.21.21", "192.168.21.24", "192.168.21.25","192.168.26.47"]
    result = ping_ips(ips)
    
    # Display results
    for ip, data in result.items():
        print(f"IP: {ip}")
        print(f"Success: {data['success']}")
        print(f"Time: {data['time']:.3f} seconds")
        if data['success']:
            print("Output excerpt:")
            output_lines = data['output'].split('\n')
            # Print a subset of the output (summary lines)
            for line in output_lines[:2]:
                print(f"  {line}")
            for line in output_lines[-3:]:
                if line:
                    print(f"  {line}")
        print("-" * 40) 