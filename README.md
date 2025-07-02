# UWatchTower Ping Monitoring System

A Python-based system that pings specified IP addresses and sends the results to a PHP API endpoint for storage and monitoring.

## Features

- Automatically pings specified IP addresses on a scheduled interval
- Sends ping results to a PHP API endpoint for storage in a database
- Runs in the background and can be scheduled to run at startup
- Tracks ping status, response time, and packet loss
- Displays real-time ping results in the console

## Setup Instructions

### 1. Requirements

- Python 3.6 or higher
- Required Python packages (see Requirements.txt)

### 2. Installation

Install required packages:

```bash
pip install -r Requirements.txt
```

### 3. Configuration

Create a `.env` file in the same directory with the following settings:

```
# PHP API Endpoint
PHP_API_URL=http://your-server.com/api/ping
```

### 4. Update IP Addresses

Edit the `automatic_ping.py` file to specify the IP addresses you want to monitor:

```python
# Define the IP addresses to ping
ips = ["192.168.21.44", "192.168.21.24", "192.168.21.25", "192.168.26.47"]
```

### 5. Running the Ping Monitor

To start the monitor:

```bash
python automatic_ping.py
```

The script will ping the specified IP addresses once immediately and then every 5 minutes.

## PHP API Requirements

The PHP API endpoint expects a POST request with the following JSON data structure:

```json
{
  "asset_id": "192.168.21.44",
  "ping_status": "up",  
  "ping_time": "0.123",
  "ping_date": "2023-05-15",
  "ping_time_offset": "14:30:45",
  "ping_packet_loss": "0%"
}
```

### PHP API Response

The PHP API should return a JSON response with a success message:

```json
{
  "success": true,
  "message": "ping created successfully"
}
```

## Scripts Description

- **automatic_ping.py**: Main script that schedules and executes ping operations
- **ping_utility.py**: Utility functions for pinging IP addresses
- **endpoint_api.py**: Functions for sending data to the PHP API endpoint

## Customization

- Change ping frequency: Modify `schedule.every(5).minutes.do(run_ping_check)` in automatic_ping.py
- Change ping timeout: Modify the `timeout` parameter in the ping_ips function call
- Change ping count: Modify the `count` parameter in the ping_ips function call 