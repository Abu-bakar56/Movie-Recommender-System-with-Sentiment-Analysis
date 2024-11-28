# Base image
FROM python:3.8-slim-buster

# Set working directory
WORKDIR /app

# Copy application files to the container
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask’s default port
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]
