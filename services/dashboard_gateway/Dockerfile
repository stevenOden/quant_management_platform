# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Add curl for health check
#RUN apt-get update && apt-get install -y curl

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the script
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]