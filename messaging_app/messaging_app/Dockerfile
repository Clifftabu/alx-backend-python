# Use an official Python base image
FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev pkg-config && \
    pip install --upgrade pip && \
    pip install -r requirements.txt


# Copy project code
COPY . /app/

# Expose port if you will run container manually
EXPOSE 8000

# Command to run the Django app using gunicorn
CMD ["python", "messaging_app/manage.py", "runserver", "0.0.0.0:8000"]
