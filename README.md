# Minecraft Server on Koyeb

This is a Docker-based Minecraft Java Edition server setup for deployment on Koyeb.

## Features

- Automatically downloads the latest Minecraft server version
- Configurable server properties
- Ready for Koyeb deployment

## Deployment to Koyeb

1. **Push to GitHub**: Commit and push this code to a GitHub repository.

2. **Create Koyeb Account**: Sign up at [koyeb.com](https://www.koyeb.com) if you haven't already.

3. **Deploy Service**:
   - Go to your Koyeb dashboard
   - Click "Create Service" > "Docker"
   - Connect your GitHub repository
   - Set the following:
     - **Dockerfile path**: `Dockerfile` (leave default)
     - **Port**: `25565` (TCP)
     - **Instance type**: Choose based on your needs (free tier has limitations)
     - **Environment variables**: Add any custom settings if needed

4. **Persistence**: For world data persistence, Koyeb supports volumes. Add a volume mount for `/minecraft` in the service settings.

5. **Scaling**: Koyeb allows horizontal scaling, but Minecraft servers typically need a single instance.

## Configuration

Edit `server.properties` to customize your server:
- `motd`: Server message
- `difficulty`: easy/medium/hard
- `max-players`: Maximum players
- `online-mode`: Set to false if you want cracked clients (not recommended)

## Local Testing

To test locally with Docker:

```bash
docker build -t minecraft-server .
docker run -p 25565:25565 minecraft-server
```

## Important Notes

- Koyeb's free tier has CPU and memory limits that may not be sufficient for a busy server
- Consider upgrading to a paid plan for better performance
- Monitor resource usage in Koyeb dashboard
- Back up your world data regularly

## Troubleshooting

- If the server fails to start, check the logs in Koyeb dashboard
- Ensure port 25565 is open and accessible
- For connection issues, verify your Minecraft client version matches the server

## License

This setup uses the official Minecraft server software. Make sure to comply with Mojang's EULA.