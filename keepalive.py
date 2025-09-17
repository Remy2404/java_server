#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import threading
import subprocess
import os
import signal
import sys

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Minecraft server is running')

    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_http_server():
    # Always use 8080 for Railway health checks
    health_port = 8080
    server = HTTPServer(('0.0.0.0', health_port), HealthCheckHandler)
    print(f"Health check server running on port {health_port}")
    server.serve_forever()

def get_fabric_server_url():
    # Fabric server launcher for 1.21.8
    return 'https://meta.fabricmc.net/v2/versions/loader/1.21.8/0.17.2/1.1.0/server/jar'

def download_fabric_server():
    fabric_url = get_fabric_server_url()
    fabric_file = 'fabric-server-mc.1.21.8-loader.0.17.2-launcher.1.1.0.jar'
    
    print(f"Downloading Fabric server from: {fabric_url}")
    import urllib.request
    response = urllib.request.urlopen(fabric_url)
    with open(fabric_file, 'wb') as f:
        f.write(response.read())
    print("Fabric server download complete")
    return fabric_file

def main():
    # Start HTTP health check server in background
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()

    # Download Fabric server jar if not exists
    jar_file = 'fabric-server-mc.1.21.8-loader.0.17.2-launcher.1.1.0.jar'
    if not os.path.exists(jar_file):
        print("Downloading Fabric Minecraft server...")
        try:
            jar_file = download_fabric_server()
            print("Download complete")
        except Exception as e:
            print(f"Download failed: {e}")
            sys.exit(1)

    # Download Fabric API if needed
    print("Checking for Fabric API...")
    exec(open('download_mods.py').read())

    # Accept EULA
    with open('eula.txt', 'w') as f:
        f.write('eula=true\n')

    # Set memory limits (conservative for Railway free tier)
    max_memory = os.environ.get('MAX_MEMORY', '1G')
    initial_memory = os.environ.get('INITIAL_MEMORY', '512M')
    
    # Minecraft server always uses 25565 (Railway will proxy it)
    minecraft_port = '25565'

    # Start Minecraft server
    print(f"Starting Minecraft server on port {minecraft_port}...")
    cmd = ['java', f'-Xmx{max_memory}', f'-Xms{initial_memory}', '-jar', jar_file, 'nogui']
    print(f"Running: {' '.join(cmd)}")

    try:
        process = subprocess.Popen(cmd)
        process.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        process.terminate()
        process.wait()

if __name__ == '__main__':
    main()