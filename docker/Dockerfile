# Multi-stage Dockerfile for Data Project
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    AIRFLOW_HOME=/opt/airflow \
    AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags \
    AIRFLOW__CORE__LOAD_EXAMPLES=false \
    AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS=false

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create airflow user
RUN useradd -m -u 50000 airflow

WORKDIR /opt/airflow

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy project code
COPY src/ /opt/app/src/
COPY setup.py /opt/app/
COPY metal_project/ /opt/airflow/dbt_project/
COPY airflow/dags/ /opt/airflow/dags/

# Install the local package
RUN pip install -e /opt/app/

# Change ownership to airflow user
RUN chown -R airflow:airflow /opt/airflow /opt/app

# Expose ports
EXPOSE 8080

CMD ["bash"]
