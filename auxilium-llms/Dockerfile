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

# Create the Streamlit configuration directory and file
RUN mkdir -p ~/.streamlit && \
    echo "[server]\nmaxUploadSize = 10240" > ~/.streamlit/config.toml

# Expose port 8501
EXPOSE 8501

# Start the App Interface
CMD ["sh", "-c", "streamlit run app/main.py"]