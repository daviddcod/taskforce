# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /usr/src/taskforce

# Install system dependencies and clean up in one layer
RUN apt-get update \
    && apt-get -y install netcat-openbsd gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Combine Python dependency installations into one layer
COPY requirements.txt /usr/src/taskforce/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install django-cors-headers mutagen mollie-api-python pillow Twisted gunicorn dj_database_url

# Add the rest of the code
COPY . /usr/src/taskforce

# Add and run as non-root user for security
RUN adduser --disabled-password --gecos '' taskforceuser
USER taskforceuser

# Your app's port number.
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "taskforce.wsgi:application"]
