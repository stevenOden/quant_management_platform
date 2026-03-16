# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the script
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]