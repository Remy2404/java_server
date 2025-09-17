#!/usr/bin/env python3

import urllib.request
import os

def download_fabric_api():
    """Download Fabric API mod for 1.21.8"""
    fabric_api_url = "https://github.com/FabricMC/fabric/releases/download/0.133.4%2B1.21.8/fabric-api-0.133.4+1.21.8.jar"
    fabric_api_file = "mods/fabric-api-0.133.4+1.21.8.jar"
    
    if not os.path.exists(fabric_api_file):
        print("Downloading Fabric API...")
        try:
            os.makedirs("mods", exist_ok=True)
            response = urllib.request.urlopen(fabric_api_url)
            with open(fabric_api_file, 'wb') as f:
                f.write(response.read())
            print("Fabric API downloaded successfully")
        except Exception as e:
            print(f"Failed to download Fabric API: {e}")
    else:
        print("Fabric API already exists")

if __name__ == "__main__":
    download_fabric_api()