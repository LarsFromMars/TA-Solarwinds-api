#!/opt/splunk/bin/python3.9
import sys
import os
import urllib3
import requests
from orionsdk import SwisClient

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_splunk_password(session_key, username, app='TA-Solarwinds-api'):
    """Get decrypted password from Splunk's passwords.conf using REST API"""
    try:
        # URL encode the username for the REST endpoint
        import urllib.parse
        encoded_username = urllib.parse.quote(username, safe='')
        
        # Make REST API call to get passwords
        splunkd_url = 'https://localhost:8089'
        endpoint = f'/servicesNS/nobody/{app}/storage/passwords/{encoded_username}?output_mode=json'
        url = splunkd_url + endpoint
        
        headers = {
            'Authorization': f'Bearer {session_key}',
            'Content-Type': 'application/json'
        }
        
        # Disable SSL verification for local Splunk instance
        response = requests.get(url, headers=headers, verify=False, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            # The password is in the entry's content
            entries = data.get('entry', [])
            if entries:
                password = entries[0].get('content', {}).get('clear_password')
                if password:
                    return password
        else:
            print(f"REST API returned status: {response.status_code}")
            
        return None
        
    except Exception as e:
        print(f"ERROR in get_splunk_password: {e}")
        return None

def main():
    # Get session key from stdin
    if not sys.stdin.isatty():
        session_key = sys.stdin.read().strip()
    else:
        session_key = None
    
    if not session_key:
        print("ERROR: No session key provided by Splunk")
        sys.exit(1)
    
    hostname = '192.168.50.99'
    username = 'admin'
    
    print(f"DEBUG: Session key length: {len(session_key)}")
    
    # Get the actual decrypted password
    password = get_splunk_password(session_key, username)
    
    if not password:
        print("ERROR: Could not retrieve decrypted password from Splunk")
        sys.exit(1)
    
    print(f"DEBUG: Retrieved decrypted password, length: {len(password)}")
    print(f"DEBUG: First 2 chars of decrypted password: {password[:2]}")
    
    try:
        swis = SwisClient(hostname, username, password, port=17774, verify=False)
        result = swis.query("SELECT TOP 1 HostName FROM Orion.OrionServers")
        print(f"Successfully connected to {hostname}. Server: {result['results'][0]['HostName']}")
        sys.exit(0)
        
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
