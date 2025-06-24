import os
import requests
from dotenv import load_dotenv
import json

# Load .env credentials
load_dotenv()
client_id = os.getenv("ACTION1_CLIENT_ID")
client_secret = os.getenv("ACTION1_CLIENT_SECRET")
org_id = os.getenv("ACTION1_ORG_ID")  # Make sure this is in your .env file

print(f"🔍 Loaded credentials:")
print(f"  Client ID: {'✅ Found' if client_id else '❌ Missing'}")
print(f"  Client Secret: {'✅ Found' if client_secret else '❌ Missing'}")
print(f"  Organization ID: {'✅ Found' if org_id else '❌ Missing'}")

if not org_id:
    print("\n❌ ERROR: ACTION1_ORG_ID not found in .env file!")
    print("Please add ACTION1_ORG_ID=your_org_id to your .env file")
    exit(1)

def make_api_request(url, headers, description="", params=None):
    """Helper function to make API requests with detailed error handling"""
    print(f"\n{'='*60}")
    print(f"🔍 Testing: {description}")
    print(f"📡 URL: {url}")
    if params:
        print(f"📋 Parameters: {params}")
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Content Type: {response.headers.get('content-type', 'Not specified')}")
        print(f"📊 Content Length: {len(response.text)}")
        
        # Handle different response types
        if response.status_code == 200:
            try:
                if response.text.strip():
                    data = response.json()
                    print("✅ SUCCESS - JSON Response:")
                    
                    # Pretty print with limited depth for large responses
                    if isinstance(data, dict) and 'items' in data:
                        print(f"📊 Total Items: {data.get('total_items', 'Unknown')}")
                        print(f"📊 Returned Items: {len(data.get('items', []))}")
                        print(f"📊 Limit: {data.get('limit', 'Unknown')}")
                        
                        # Show first few items
                        items = data.get('items', [])
                        if items:
                            print("\n🖥️  First endpoint details:")
                            first_item = items[0]
                            for key, value in first_item.items():
                                print(f"  {key}: {value}")
                            
                            if len(items) > 1:
                                print(f"\n... and {len(items) - 1} more endpoints")
                    else:
                        print(json.dumps(data, indent=2))
                    
                    return data
                else:
                    print("⚠️  SUCCESS but empty response")
                    return None
            except requests.exceptions.JSONDecodeError:
                print("✅ SUCCESS but non-JSON response:")
                print(response.text[:500])
                return response.text
        
        elif response.status_code == 403:
            print("❌ FORBIDDEN - No permission to access this endpoint")
            try:
                error_data = response.json()
                print("Error details:")
                print(json.dumps(error_data, indent=2))
            except:
                print("Raw response:")
                print(response.text[:300])
            
        elif response.status_code == 401:
            print("❌ UNAUTHORIZED - Token invalid or expired")
            try:
                error_data = response.json()
                print("Error details:")
                print(json.dumps(error_data, indent=2))
            except:
                print("Raw response:")
                print(response.text[:300])
            
        elif response.status_code == 400:
            print("❌ BAD REQUEST - Invalid parameters or request format")
            try:
                error_data = response.json()
                print("Error details:")
                print(json.dumps(error_data, indent=2))
            except:
                print("Raw response:")
                print(response.text[:300])
            
        elif response.status_code == 404:
            print("❌ NOT FOUND - Endpoint doesn't exist or org ID is wrong")
            print("Raw response:")
            print(response.text[:300])
            
        else:
            print(f"❌ ERROR {response.status_code}")
            print("Raw response:")
            print(response.text[:300])
            
    except requests.exceptions.RequestException as e:
        print(f"❌ REQUEST ERROR: {e}")
    
    return None

# Get access token
print("\n🔐 Getting access token...")
auth_url = "https://app.eu.action1.com/api/3.0/oauth2/token"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {
    "client_id": client_id,
    "client_secret": client_secret
}

try:
    response = requests.post(auth_url, headers=headers, data=data)
    response.raise_for_status()
    auth_data = response.json()
    access_token = auth_data["access_token"]
    
    print("✅ Access token retrieved successfully")
    print(f"🔑 Token length: {len(access_token)}")
    print(f"🔑 Token starts with: {access_token[:30]}...")
except Exception as e:
    print(f"❌ Failed to get access token: {e}")
    exit(1)

# Prepare authorization header
auth_headers = {"Authorization": f"Bearer {access_token}"}

# Test the correct endpoint from the documentation
base_url = "https://app.eu.action1.com/api/3.0"

print(f"\n{'='*80}")
print("🚀 TESTING ACTION1 ENDPOINTS API")
print(f"🏢 Organization ID: {org_id}")
print(f"{'='*80}")

# Basic endpoints call
endpoints_url = f"{base_url}/endpoints/managed/{org_id}"
result = make_api_request(endpoints_url, auth_headers, "Get all managed endpoints")

if result:
    print(f"\n{'='*60}")
    print("🎯 TESTING WITH DIFFERENT PARAMETERS")
    print(f"{'='*60}")
    
    # Test with limit parameter
    params = {"limit": 5}
    make_api_request(endpoints_url, auth_headers, "Get first 5 endpoints", params)
else:
    print(f"\n{'='*60}")
    print("🔍 TROUBLESHOOTING SUGGESTIONS")
    print(f"{'='*60}")
    
    print("\n💡 Possible issues:")
    print("1. ❌ Organization ID might be incorrect")
    print("2. ❌ Your user account lacks 'view_endpoints' permission")
    print("3. ❌ API client doesn't have proper scopes configured")
    print("4. ❌ Organization might have API restrictions")
    
    print(f"\n🔧 Things to check:")
    print(f"• Verify your org ID in Action1 dashboard: {org_id}")
    print("• Check user permissions include 'view_endpoints'")
    print("• Verify API client configuration in Action1 settings")
    print("• Contact Action1 support if permissions look correct")

print(f"\n{'='*80}")
print("📋 QUICK REFERENCE")
print(f"{'='*80}")
print("Available filters you can use:")
print("• status: Connected, Disconnected, Pending Uninstall")
print("• online_status: SUCCESS, WARNING, ERROR")
print("• update_status: SUCCESS, WARNING, ERROR")
print("• vulnerability_status: SUCCESS, WARNING, ERROR")
print("• reboot_required: Yes, No") 
print("• os: Windows 10, Windows 11, macOS, etc.")
print("• limit: number (page size)")
print("• from: number (pagination offset)")
print("• filter: string (search term)")
print("• fields: *, missing_updates, vulnerabilities")