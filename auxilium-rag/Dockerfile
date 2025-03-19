# Uses the official Python 3.11 base image
FROM python:3.11-slim

# Sets the working directory
WORKDIR /app

# Updates packages, installs necessary dependencies, and cleans caches in a single RUN command to reduce middle layers
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Install the libraries
RUN pip install -r requirements.txt && \
    rm -rf /root/.cache/pip

# Expose port 7997
EXPOSE 7997

# Start the API and run the tests
CMD ["sh", "-c", "uvicorn rag_api:app --host 0.0.0.0 --port 7997; tail -f /dev/null"]