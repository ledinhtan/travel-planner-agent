# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt setup.py ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Command to run the FastAPI backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]