# Dockerfile for sandboxed Python execution
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Create a non-root user for security
RUN useradd -m -u 1000 sandboxuser

# Install basic packages (can be extended as needed)
RUN pip install --no-cache-dir numpy pandas matplotlib scipy

# Switch to non-root user
USER sandboxuser

# Default command
CMD ["python"]
