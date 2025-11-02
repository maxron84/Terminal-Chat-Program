#!/bin/bash
# Docker Cleanup and Rebuild Script for Terminal Chat Program
# Use this if you encounter "ContainerConfig" errors or restart issues

echo "=== Terminal Chat Program - Docker Rebuild Script ==="
echo ""
echo "This script will:"
echo "1. Stop and remove existing containers"
echo "2. Remove old images"
echo "3. Clean up volumes (optional)"
echo "4. Rebuild from scratch"
echo ""

# Stop and remove containers
echo "Step 1: Stopping containers..."
docker-compose down 2>/dev/null || docker compose down 2>/dev/null || true

# Remove specific container if it exists
echo "Step 2: Removing old container..."
docker rm -f vibe-chat-server 2>/dev/null || docker rm -f 23055f9a3c2c_vibe-chat-server 2>/dev/null || true

# Remove old image
echo "Step 3: Removing old image..."
docker rmi vibe-chat:latest 2>/dev/null || true

# Ask about volumes
read -p "Do you want to clean volumes (will delete chat history)? (y/N): " clean_volumes
if [[ $clean_volumes == "y" || $clean_volumes == "Y" ]]; then
    echo "Step 4: Removing volumes..."
    docker volume rm vibe-chat-shared vibe-chat-logs 2>/dev/null || true
else
    echo "Step 4: Keeping volumes (chat history preserved)"
fi

# Check for .env file
if [ ! -f .env ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please edit .env and set a strong CHAT_PASSWORD before continuing!"
    read -p "Press Enter after editing .env..."
fi

# Rebuild and start
echo ""
echo "Step 5: Building fresh image..."
docker-compose build --no-cache || docker compose build --no-cache

echo ""
echo "Step 6: Starting services..."
docker-compose up -d || docker compose up -d

echo ""
echo "=== Checking status ===="
sleep 3
docker-compose ps || docker compose ps

echo ""
echo "=== View logs with: ==="
echo "docker-compose logs -f chat-server"
echo ""
echo "=== Connect clients with: ==="
echo "python3 bin/vibe-chat.py"
echo ""
echo "Done!"