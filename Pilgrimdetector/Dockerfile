# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy all project files
COPY . .

# Run Flask
CMD ["python", "app.py"]