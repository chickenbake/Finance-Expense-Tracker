# Create this file: backend/Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port (Cloud Run uses PORT env variable)
EXPOSE 8080

# Set default PORT if not provided by Cloud Run
ENV PORT=8080

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]