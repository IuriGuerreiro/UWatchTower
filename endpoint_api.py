import requests
import json
import datetime
import os
from dotenv import load_dotenv

# Load .env file to get the PHP API URL and token
load_dotenv()

# Define the PHP API URL and token
PHP_API_URL = os.getenv("PHP_API_URL")

def send_ping_results(ip, ping_result):
    print(f"\n{'='*60}")
    print(f"📡 Sending ping results for {ip} to PHP API")
    
    # Verificar URL da API
    if not PHP_API_URL:
        print("❌ ERROR: PHP_API_URL not configured in .env file!")
        return {"success": False, "message": "API URL not configured"}
    
    # Calculate packet loss
    packet_loss = "0%"
    if ping_result['success'] and "packet loss" in ping_result['output'].lower():
        output_lines = ping_result['output'].split('\n')
        for line in output_lines:
            if "packet loss" in line.lower():
                parts = line.split('%')
                if len(parts) > 1:
                    for part in parts[0].split(' '):
                        if part.strip() and part.strip().replace('.', '', 1).isdigit():
                            packet_loss = f"{part}%"
                            break
    
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%Y-%m-%d")
    
    # Prepare data
    data = {
        'asset_id': 911,
        'ping_status': 'up' if ping_result['success'] else 'down',
        'ping_time': f"{ping_result['time']:.3f}" if ping_result['success'] else None,
        'ping_date': current_date,
        'ping_time_offset': current_datetime.strftime("%H:%M:%S"),
        'ping_packet_loss': packet_loss,
    }
    
    # Debug output
    print(f"📤 Data being sent:")
    # Don't show the full token in debug output
    debug_data = data.copy()
    print(json.dumps(debug_data, indent=2))
    
    headers = {
	"host": "127.0.0.1:8086",
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"accept-language": "pt-PT,pt;q=0.8,en;q=0.5,en-US;q=0.3",
	"accept-encoding": "gzip, deflate, br, zstd",
	"dnt": "1",
	"sec-gpc": "1",
	"connection": "keep-alive",
	"cookie": "********",
	"upgrade-insecure-requests": "1",
	"sec-fetch-dest": "document",
	"sec-fetch-mode": "navigate",
	"sec-fetch-site": "none",
	"sec-fetch-user": "?1",
	"priority": "u=0, i",
	"pragma": "no-cache",
	"cache-control": "no-cache"
    }
    
    try:
        print("🚀 Sending POST request...")
        response = requests.post(PHP_API_URL, json=data, headers=headers, timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        # Log raw response
        print(f"📝 Raw Response: {response.text[:500]}")
        
        if response.status_code in [200, 201]:
            print("✅ SUCCESS: Ping data sent to API")
            try:
                response_data = response.json()
                print(f"📨 Response Data: {json.dumps(response_data, indent=2)}")
                return response_data
            except json.JSONDecodeError:
                print("⚠️ Response is not valid JSON")
                return {"success": True, "message": "Data sent but response not JSON"}
        elif response.status_code == 401:
            print("❌ AUTHENTICATION ERROR: Invalid or missing token")
            return {"success": False, "message": "Authentication failed - check API token"}
        elif response.status_code == 403:
            print("❌ AUTHORIZATION ERROR: Token valid but access denied")
            return {"success": False, "message": "Access denied - insufficient permissions"}
        else:
            print(f"❌ HTTP ERROR: {response.status_code}")
            try:
                error_data = response.json()
                print(f"❌ Error Response: {json.dumps(error_data, indent=2)}")
                return error_data
            except:
                print(f"❌ Raw Error Response: {response.text}")
                return {"success": False, "message": f"HTTP {response.status_code}: {response.text}"}
                
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT: Request took too long")
        return {"success": False, "message": "Request timeout"}
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Cannot connect to API")
        return {"success": False, "message": "Connection error"}
    except requests.exceptions.RequestException as e:
        print(f"❌ REQUEST ERROR: {e}")
        return {"success": False, "message": str(e)}