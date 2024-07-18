# Use the official Python image as a base
FROM python:3.8

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        libpq-dev \
        --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Pass ALLOWED_HOSTS environment variable
ENV ALLOWED_HOSTS=62.72.19.182,administration23wer21.pronap.store

# Start the Django application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "pronap_admin.wsgi:application"]
