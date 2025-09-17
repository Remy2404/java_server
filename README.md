# Minecraft Server on Railway/Koyeb

This is a Docker-based Minecra## Important Notes

- Railway/Koyeb free tiers have CPU and memory limits - **modded Minecraft servers often need 2-4GB RAM**
- Consider upgrading to paid plans for better performance and stability
- Monitor resource usage in your dashboard - check for OOM (Out of Memory) errors
- Back up your world data regularly
- The HTTP server only responds to health checks - actual Minecraft connections use TCP Edition server setup with a health check HTTP server for deployment on Railway or Koyeb.

## Features

- Automatically downloads the latest Minecraft server version
- Includes HTTP health check server to prevent timeouts
- Uses lightweight Alpine Linux base image for better performance
- Configurable server properties
- Ready for Railway/Koyeb deployment

## Deployment

### Railway Deployment

1. **Push to GitHub**: Commit and push this code to a GitHub repository.

2. **Connect to Railway**: 
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Railway will auto-detect the Dockerfile

3. **Environment Variables**:
   - `PORT`: Set to `8080` (for health checks)
   - `MEMORY`: Set to `1G` or `2G` depending on your plan

4. **Port Configuration**: Railway will use the PORT variable for HTTP health checks. Minecraft runs on 25565 internally.

5. **Public URL**: Railway provides a domain, but for Minecraft connections, you'll need the Railway TCP proxy or use the internal networking.

### Koyeb Deployment

1. **Push to GitHub**: Commit and push this code to a GitHub repository.

2. **Create Koyeb Account**: Sign up at [koyeb.com](https://www.koyeb.com)

3. **Deploy Service**:
   - Go to dashboard → Create Service → Docker
   - Connect your GitHub repository
   - Set port: `8080` (HTTP for health checks)
   - Add TCP port 25565 for Minecraft connections
   - Environment variables: `MEMORY=1G`

4. **Persistence**: Add a volume mount for `/minecraft` to persist world data.

## Configuration

Edit `server.properties` to customize your server:
- `motd`: Server message
- `difficulty`: easy/medium/hard
- `max-players`: Maximum players (keep low for free tiers)
- `online-mode`: Set to false if you want cracked clients (not recommended)

## Environment Variables

- `PORT`: HTTP port for health checks (default: 8080)
- `MEMORY`: Java heap size (default: 2G - increased for modded servers)

## Local Testing

To test locally with Docker:

```bash
docker build -t minecraft-server .
docker run -p 8080:8080 -p 25565:25565 -e PORT=8080 minecraft-server
```

Connect Minecraft to `localhost:25565`

## Important Notes

- Railway/Koyeb free tiers have CPU and memory limits
- Consider upgrading to paid plans for better performance
- Monitor resource usage in your dashboard
- Back up your world data regularly
- The HTTP server only responds to health checks - actual Minecraft connections use TCP

## Troubleshooting

- **502 Bad Gateway**: Usually means the HTTP health check server isn't responding
- **Out of Memory (OOM) errors**: Increase MEMORY environment variable or upgrade your plan
- **Server crashes**: Check memory allocation and mod compatibility
- **Connection refused**: Ensure port 25565 is properly exposed
- **Slow performance**: Increase MEMORY or upgrade your plan
- **Railway deployment failures**: Check Railway metrics for memory usage patterns

## License

This setup uses the official Minecraft server software. Make sure to comply with Mojang's EULA.