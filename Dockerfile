# Dockerfile for sandboxed Python execution
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Create a non-root user for security
RUN useradd -m -u 1000 sandboxuser

# Switch to non-root user
USER sandboxuser

# Default command
CMD ["python"]
