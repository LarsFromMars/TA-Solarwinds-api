from orionsdk import SwisClient
import getpass

def main():
    hostname = '192.168.50.99'
    
    username = input(f"Username for {hostname}: ")
    password = getpass.getpass("Password: ")
    
    try:
        swis = SwisClient(hostname, username, password, port=17774)
        swis.query("SELECT TOP 1 HostName FROM Orion.OrionServers")
        print(f"Successfully connected to {hostname}")
        return True
        
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    main()
