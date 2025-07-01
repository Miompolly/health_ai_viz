# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies (optional but good for compatibility)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install psycopg2-binary
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Ensure the static directory exists
RUN mkdir -p /app/static

# Collect static files (optional here; also in docker-compose command)
# RUN python manage.py collectstatic --noinput

# Expose the port used by Gunicorn
EXPOSE 8000

# Start with Gunicorn (overridable in docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecohub_bn.wsgi:application"]

