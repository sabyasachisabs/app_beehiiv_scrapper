# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actor code
COPY src/ ./src/
COPY scrape_beehiiv.py ./

# Set the main script as entrypoint
CMD ["python", "src/main.py"]

