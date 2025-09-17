# Use OpenJDK 21 slim as base image (Minecraft 1.20+ requires Java 17+)
FROM openjdk:21-slim

# Set working directory
WORKDIR /minecraft

# Install curl, jq, and python3 for downloading and keepalive
RUN apt-get update && apt-get install -y curl jq python3 && rm -rf /var/lib/apt/lists/*

# Copy entrypoint script
COPY entrypoint.sh /minecraft/entrypoint.sh
COPY keepalive.py /minecraft/keepalive.py
RUN chmod +x /minecraft/entrypoint.sh /minecraft/keepalive.py

# Copy server properties
COPY server.properties /minecraft/server.properties

# Expose Minecraft port
EXPOSE 25565

# Set entrypoint
ENTRYPOINT ["python3", "/minecraft/keepalive.py"]