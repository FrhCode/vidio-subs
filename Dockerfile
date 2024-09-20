# Use the official Python 3.10.11 image as a base
FROM python:3.10.11-slim

# Set the working directory in the container
WORKDIR /app

# Install ffmpeg and any other system dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy only the requirements.txt first to leverage Docker cache
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code
COPY . /app

# Run the Python script when the container launches
CMD ["python", "./index.py"]
