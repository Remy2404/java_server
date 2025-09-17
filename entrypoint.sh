#!/bin/bash

# Function to get latest Minecraft version
get_latest_version() {
    curl -s https://launchermeta.mojang.com/mc/game/version_manifest.json | \
    jq -r '.latest.release'
}

# Function to get server download URL
get_server_url() {
    local version=$1
    local version_manifest=$(curl -s "https://launchermeta.mojang.com/mc/game/version_manifest.json")
    local version_url=$(echo "$version_manifest" | jq -r ".versions[] | select(.id == \"$version\") | .url")
    curl -s "$version_url" | jq -r '.downloads.server.url'
}

# Download server jar if not exists
if [ ! -f "minecraft_server.jar" ]; then
    echo "Downloading latest Minecraft server..."
    LATEST_VERSION=$(get_latest_version)
    echo "Latest version: $LATEST_VERSION"
    SERVER_URL=$(get_server_url "$LATEST_VERSION")
    echo "Downloading from: $SERVER_URL"
    curl -o minecraft_server.jar "$SERVER_URL"
fi

# Accept EULA
echo "eula=true" > eula.txt

# Set memory limits (adjust as needed for your plan)
MEMORY="1G"

# Run Minecraft server
echo "Starting Minecraft server..."
exec java -Xmx${MEMORY} -Xms${MEMORY} -jar minecraft_server.jar nogui