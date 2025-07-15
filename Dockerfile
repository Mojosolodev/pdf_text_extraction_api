# Use Python 3.13 slim base image to match Render’s Python 3.13.4
FROM python:3.13-slim

# Install system dependencies for blis and spacy compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libblas-dev \
    liblapack-dev \
    libc-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]