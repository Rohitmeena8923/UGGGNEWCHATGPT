# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app code
COPY . .

# Expose port 5000 for Flask (agar Flask use ho raha hai)
EXPOSE 5000

# Run your main bot script
CMD ["python", "main.py"]