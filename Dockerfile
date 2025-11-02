# Vibe Cozy Chat - Docker Image
FROM python:3.9-slim

# Set metadata
LABEL maintainer="Vibe Cozy Chat Team"
LABEL description="Secure encrypted terminal chat application"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Copy application files
COPY src/ /app/src/
COPY bin/ /app/bin/
COPY data/ /app/data/

# Create necessary directories
RUN mkdir -p /app/data/inbox /app/data/outbox /app/data/shared /app/logs

# Set permissions
RUN chmod -R 755 /app/src /app/bin

# Expose default chat port
EXPOSE 4444

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python3 -c "import socket; s=socket.socket(); s.settimeout(1); s.connect(('localhost', 4444)); s.close()" || exit 1

# Default command (server mode)
# Can be overridden with docker run arguments
ENTRYPOINT ["python3", "src/modular/cozy_secure_chat_modular.py"]
CMD ["listen", "4444", "changeMe123", "Server"]