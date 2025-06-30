import time
import schedule
from ping_utility import ping_ips

def run_ping_check():
    """
    Run ping checks on the defined IP addresses
    """
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Running scheduled ping check...")
    
    # Define the IP addresses to ping - you can modify this list as needed
    ips = ["192.168.21.44", "192.168.21.24", "192.168.21.25", "192.168.26.47"]
    
    # Run the ping check
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

def start_scheduler():
    """
    Start the scheduler to run ping checks every 5 minutes
    """
    print("Starting automatic ping scheduler...")
    print(f"First ping will run immediately, then every 5 minutes.")
    
    # Run once immediately
    run_ping_check()
    
    # Schedule to run every 5 minutes
    schedule.every(5).minutes.do(run_ping_check)
    
    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")

if __name__ == "__main__":
    start_scheduler() 