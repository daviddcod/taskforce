# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONUNBUFFERED 1  # Prevents Python from buffering stdout and stderr (equivalent to python -u option)

# Set work directory
WORKDIR /usr/src/taskforce

# Install system dependencies
# Specify the version of netcat you want to install
RUN apt-get update \
    && apt-get -y install netcat-openbsd gcc \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /usr/src/taskforce/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
RUN pip install django-cors-headers
RUN pip install mutagen
RUN pip install mollie
RUN pip install mollie-api-python

# Add the rest of the code
COPY . /usr/src/taskforce

# Add and run as non-root user for security
RUN adduser --disabled-password --gecos '' taskforceuser
USER taskforceuser

# Your app's port number.
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "taskforce.wsgi:application"]
