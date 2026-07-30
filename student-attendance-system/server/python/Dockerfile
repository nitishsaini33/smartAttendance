# Use official Python slim image
FROM python:3.11-slim

# Install system dependencies required by OpenCV headless & insightface
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgomp1 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for layer caching (path relative to repo root)
COPY student-attendance-system/server/python/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (path relative to repo root)
COPY student-attendance-system/server/python/ .

# Expose port
EXPOSE 8080

# Start with gunicorn (Railway injects $PORT automatically)
CMD gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 1 api_server:app
