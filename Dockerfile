# Use Eclipse Temurin JDK 21 Alpine for smaller image size
FROM eclipse-temurin:21-jdk-alpine

# Set working directory
WORKDIR /minecraft

# Install curl, jq, and python3 for downloading and keepalive
RUN apk add --no-cache curl jq python3

# Copy scripts
COPY keepalive.py /minecraft/keepalive.py
COPY download_mods.py /minecraft/download_mods.py
RUN chmod +x /minecraft/keepalive.py

# Copy server properties
COPY server.properties /minecraft/server.properties

# Expose ports
EXPOSE 8080 25565

# Set entrypoint
ENTRYPOINT ["python3", "/minecraft/keepalive.py"]