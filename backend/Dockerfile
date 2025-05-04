# Backend Dockerfile
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose port for the backend
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]
