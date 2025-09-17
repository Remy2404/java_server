# Use OpenJDK 21 slim as base image (Minecraft 1.20+ requires Java 17+)
FROM openjdk:21-slim

# Set working directory
WORKDIR /minecraft

# Install curl, jq, python3, and requests for downloading and keepalive
RUN apt-get update && apt-get install -y curl jq python3 python3-pip && \
    pip3 install requests && \
    rm -rf /var/lib/apt/lists/*

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