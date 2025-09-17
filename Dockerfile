# Use OpenJDK 21 as base image (Minecraft 1.20+ requires Java 17+)
FROM openjdk:21-jre-slim

# Set working directory
WORKDIR /minecraft

# Install curl and jq for downloading
RUN apt-get update && apt-get install -y curl jq && rm -rf /var/lib/apt/lists/*

# Copy entrypoint script
COPY entrypoint.sh /minecraft/entrypoint.sh
RUN chmod +x /minecraft/entrypoint.sh

# Copy server properties
COPY server.properties /minecraft/server.properties

# Expose Minecraft port
EXPOSE 25565

# Set entrypoint
ENTRYPOINT ["/minecraft/entrypoint.sh"]