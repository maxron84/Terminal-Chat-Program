# 🐳 Docker Deployment Guide

Complete guide for deploying Vibe Cozy Chat using Docker and Docker Compose.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Configuration](#configuration)
3. [Production Setup](#production-setup)
4. [Management](#management)
5. [Security](#security)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Topics](#advanced-topics)

---

## Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 1.29+
- Port 4444 available

### Deploy in 3 Steps

```bash
# 1. Configure
cp .env.example .env
echo "CHAT_PASSWORD=$(openssl rand -hex 32)" >> .env

# 2. Deploy
docker-compose up -d

# 3. Connect
python3 bin/vibe-chat.py
```

That's it! Server is running.

---

## Configuration

### Environment Variables

Edit `.env` file:

```bash
# Required - use strong password!
CHAT_PASSWORD=your_strong_password_here

# Optional
SERVER_USERNAME=ChatServer
CHAT_PORT=4444
```

Generate strong password:
```bash
openssl rand -hex 32
```

### Docker Compose Files

**docker-compose.yml** - Production (server only)
- Resource limits
- Health monitoring
- Log rotation
- Auto-restart

**docker-compose.dev.yml** - Development (server + clients)
- Interactive testing
- Multiple clients
- No resource limits

---

## Production Setup

### Production Features

✅ **Resource Management**
- CPU: 1.0 cores max (0.25 reserved)
- Memory: 512MB max (128MB reserved)

✅ **High Availability**
- Restart policy: `unless-stopped`
- Health checks: every 30s
- Automatic recovery

✅ **Data Persistence**
- Named volumes (not local paths)
- Shared files: `vibe-chat-shared`
- Server logs: `vibe-chat-logs`

✅ **Security**
- Required password validation
- Read-only outbox mount
- Isolated network
- No interactive terminals

✅ **Logging**
- JSON format
- Max size: 10MB per file
- Rotation: 3 files (30MB total)

### Production Checklist

Before deploying:
- [ ] Strong password set
- [ ] Firewall configured
- [ ] TLS/SSL enabled (if public - NOT RECOMMENDED)
- [ ] Backup strategy in place
- [ ] Resource limits appropriate
- [ ] Health checks working
- [ ] Logs rotation enabled

---

## Management

### Start/Stop

```bash
# Start server
docker-compose up -d

# Stop server
docker-compose stop

# Restart server
docker-compose restart

# Stop and remove
docker-compose down
```

### Logs

```bash
# Follow logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Save to file
docker-compose logs > server-logs.txt
```

### Monitoring

```bash
# Check status
docker-compose ps

# Resource usage
docker stats vibe-chat-server

# Health status
docker inspect vibe-chat-server --format='{{.State.Health.Status}}'

# Detailed health
docker inspect vibe-chat-server --format='{{json .State.Health}}' | jq
```

### Updates

```bash
# Pull new code
git pull

# Rebuild and deploy
docker-compose build
docker-compose up -d

# Clean old images
docker image prune
```

### Backup & Restore

**Backup:**
```bash
mkdir -p backups

# Backup shared files
docker run --rm \
  -v vibe-chat-shared:/source:ro \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/shared-$(date +%Y%m%d-%H%M%S).tar.gz -C /source .

# Backup logs
docker run --rm \
  -v vibe-chat-logs:/source:ro \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/logs-$(date +%Y%m%d-%H%M%S).tar.gz -C /source .
```

**Restore:**
```bash
# Stop server
docker-compose down

# Restore shared files
docker run --rm \
  -v vibe-chat-shared:/target \
  -v $(pwd)/backups:/backup \
  alpine tar xzf /backup/shared-YYYYMMDD-HHMMSS.tar.gz -C /target

# Start server
docker-compose up -d
```

---

## Security

### 1. Strong Password

```bash
# Generate secure password
openssl rand -hex 32 > .password
chmod 600 .password

# Add to .env
echo "CHAT_PASSWORD=$(cat .password)" >> .env
```

### 2. Firewall Configuration

```bash
# Allow specific subnet only
sudo ufw allow from 192.168.1.0/24 to any port 4444

# Or use fail2ban
sudo apt install fail2ban
```

### 3. Network Isolation

The docker-compose setup includes:
- Isolated bridge network
- Internal communication only
- No public exposure by default

### 4. TLS/SSL (For Public Internet)

⚠️ **This app is for PRIVATE networks only!**

If you must expose it publicly:

**Option A: nginx reverse proxy**
```nginx
upstream chat_server {
    server localhost:4444;
}

server {
    listen 443 ssl;
    server_name chat.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://chat_server;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Option B: traefik**
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.tcp.routers.chat.rule=HostSNI(`chat.example.com`)"
  - "traefik.tcp.routers.chat.tls=true"
  - "traefik.tcp.routers.chat.tls.certresolver=letsencrypt"
```

### 5. Regular Updates

```bash
# Update system
sudo apt update && sudo apt upgrade

# Update Docker
docker-compose pull
docker-compose up -d
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs

# Common issues:
# 1. Port already in use
sudo lsof -i :4444

# 2. Password not set
grep CHAT_PASSWORD .env

# 3. Permissions
ls -la data/
```

### Can't Connect

```bash
# Check if running
docker-compose ps

# Check health
docker inspect vibe-chat-server --format='{{.State.Health.Status}}'

# Test port
telnet localhost 4444
```

### High CPU/Memory

```bash
# Check resources
docker stats vibe-chat-server

# Adjust in docker-compose.yml:
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 1G
```

### Permission Issues

```bash
# Fix data directory
sudo chown -R 1000:1000 data/
chmod -R 755 data/
```

### Logs Not Appearing

```bash
# Ensure log directory exists
mkdir -p logs
chmod 777 logs

# Check container logs
docker exec -it vibe-chat-server ls -la /app/logs
```

---

## Advanced Topics

### Docker Standalone (Without Compose)

```bash
# Build
docker build -t vibe-chat:latest .

# Run server
docker run -d \
  --name vibe-chat-server \
  -p 4444:4444 \
  -v vibe-chat-shared:/app/data/shared \
  -v vibe-chat-logs:/app/logs \
  -e CHAT_PASSWORD=your_password \
  vibe-chat:latest listen 4444 your_password Admin

# Run client (interactive)
docker run -it --rm \
  --network host \
  vibe-chat:latest connect localhost 4444 your_password Alice
```

### Development Setup

```bash
# Use dev compose file
docker-compose -f docker-compose.dev.yml up

# With test clients
docker-compose -f docker-compose.dev.yml --profile clients up

# Attach to client
docker attach vibe-chat-client-1
# Detach: Ctrl+P, Ctrl+Q
```

### Performance Tuning

**High Traffic:**
```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 256M
```

**Low Resources:**
```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 256M
    reservations:
      cpus: '0.1'
      memory: 64M
```

### Monitoring Integration

**Prometheus + Grafana:**

Add to `docker-compose.yml`:

```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - chat-network
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    networks:
      - chat-network
```

### Custom Dockerfile

For specific needs:

```dockerfile
FROM python:3.11-alpine

# Install additional tools
RUN apk add --no-cache openssl curl

# Copy application
COPY . /app
WORKDIR /app

# Custom entrypoint
ENTRYPOINT ["python3", "src/modular/cozy_secure_chat_modular.py"]
CMD ["listen", "4444", "changeMe", "Server"]
```

Build:
```bash
docker build -f Dockerfile.custom -t vibe-chat:custom .
```

### Multiple Servers

```bash
# Server 1 on port 4444
docker run -d --name chat-server-1 \
  -p 4444:4444 \
  -e CHAT_PASSWORD=pass1 \
  vibe-chat:latest listen 4444 pass1 Admin1

# Server 2 on port 4445
docker run -d --name chat-server-2 \
  -p 4445:4444 \
  -e CHAT_PASSWORD=pass2 \
  vibe-chat:latest listen 4444 pass2 Admin2
```

### Cleanup

```bash
# Stop and remove containers
docker-compose down

# Remove volumes (⚠️ DELETES DATA!)
docker-compose down -v

# Remove images
docker rmi vibe-chat:latest

# Clean everything
docker system prune -a --volumes
```

---

## Quick Reference

### Essential Commands

```bash
# Deploy
docker-compose up -d

# Logs
docker-compose logs -f

# Status
docker-compose ps

# Stop
docker-compose down

# Backup
docker run --rm -v vibe-chat-shared:/s:ro -v $(pwd)/backups:/b alpine tar czf /b/backup-$(date +%Y%m%d).tar.gz -C /s .

# Restore
docker run --rm -v vibe-chat-shared:/s -v $(pwd)/backups:/b alpine tar xzf /b/backup-YYYYMMDD.tar.gz -C /s
```

### File Locations

```
Container:
  /app/src/              - Application code
  /app/data/shared/      - Shared files
  /app/data/outbox/      - Upload staging
  /app/logs/             - Server logs

Host (volumes):
  vibe-chat-shared       - Shared files
  vibe-chat-logs         - Server logs
```

### Ports

- **4444** - Default chat port (configurable)

### Environment Variables

- `CHAT_PASSWORD` - Required, shared encryption key
- `SERVER_USERNAME` - Server display name (default: ChatServer)
- `CHAT_PORT` - Server port (default: 4444)

---

## Additional Resources

- [Main README](../README.md) - Project overview
- [Security Assessment](security/SECURITY_ASSESSMENT.md) - Security details
- [Architecture](MODULAR_STRUCTURE.md) - Code structure
- [Docker Documentation](https://docs.docker.com/) - Official Docker docs
- [Docker Compose Spec](https://docs.docker.com/compose/compose-file/) - Compose reference

---

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/vibe-cozy-chat/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/vibe-cozy-chat/discussions)
- **Security**: See [SECURITY.md](../SECURITY.md)

---

**Happy Dockerizing! 🐳**