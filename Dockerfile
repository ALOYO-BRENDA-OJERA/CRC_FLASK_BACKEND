# Use official Python Alpine image
FROM python:3.13-alpine3.20

# Install system dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev libmysqlclient-dev mariadb-connector-c-dev

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the Flask port
EXPOSE 5000

# Run the app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
