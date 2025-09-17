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
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"Health check server running on port {port}")
    server.serve_forever()

def get_latest_version():
    import urllib.request
    import json
    response = urllib.request.urlopen('https://launchermeta.mojang.com/mc/game/version_manifest.json')
    data = json.loads(response.read().decode())
    return data['latest']['release']

def get_server_url(version):
    import urllib.request
    import json
    manifest_response = urllib.request.urlopen('https://launchermeta.mojang.com/mc/game/version_manifest.json')
    manifest_data = json.loads(manifest_response.read().decode())
    versions = manifest_data['versions']
    version_url = next(v['url'] for v in versions if v['id'] == version)
    version_response = urllib.request.urlopen(version_url)
    version_data = json.loads(version_response.read().decode())
    return version_data['downloads']['server']['url']

def main():
    # Start HTTP health check server in background
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()

    # Download server jar if not exists
    jar_file = 'minecraft_server.jar'
    if not os.path.exists(jar_file):
        print("Downloading latest Minecraft server...")
        try:
            latest_version = get_latest_version()
            print(f"Latest version: {latest_version}")
            server_url = get_server_url(latest_version)
            print(f"Downloading from: {server_url}")

            import urllib.request
            response = urllib.request.urlopen(server_url)
            with open(jar_file, 'wb') as f:
                f.write(response.read())
            print("Download complete")
        except Exception as e:
            print(f"Download failed: {e}")
            sys.exit(1)

    # Accept EULA
    with open('eula.txt', 'w') as f:
        f.write('eula=true\n')

    # Set memory limits
    memory = os.environ.get('MEMORY', '1G')

    # Start Minecraft server
    print("Starting Minecraft server...")
    cmd = ['java', f'-Xmx{memory}', f'-Xms{memory}', '-jar', jar_file, 'nogui']
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