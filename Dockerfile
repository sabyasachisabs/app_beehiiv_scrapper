# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies directly
RUN pip install --no-cache-dir \
    requests>=2.31.0 \
    beautifulsoup4>=4.12.0 \
    lxml>=4.9.0 \
    apify>=1.0.0

# Copy the actor code
COPY src/ ./src/
COPY scrape_beehiiv.py ./

# Set the main script as entrypoint
CMD ["python", "src/main.py"]

