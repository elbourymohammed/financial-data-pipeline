#!/bin/bash
# Script to initialize Docker environment for the first time

set -e

echo "Initializing Data Project Docker Environment..."

cd "$(dirname "$0")"

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Create .env symlink to root env file if needed
if [ ! -f .env ]; then
    if [ -f ../.env ]; then
        ln -sf ../.env .env
        echo "Linked .env from project root"
    else
        echo "Creating .env file from template..."
        cp .env.example .env
        echo "Created .env file. Please review and update if necessary."
    fi
else
    echo ".env already exists"
fi

# Create .dbt directory if it doesn't exist
if [ ! -d .dbt ]; then
    echo "Creating .dbt directory..."
    mkdir -p .dbt
fi

# Build images
echo "Building Docker images..."
docker-compose build

# Start services
echo "Starting services..."
docker-compose up -d

# Wait for PostgreSQL
echo "Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
    if docker-compose exec -T postgres pg_isready -U airflow > /dev/null 2>&1; then
        echo "PostgreSQL is ready"
        break
    fi
    echo "Waiting... ($i/30)"
    sleep 2
done

# Initialize Airflow database
echo "Initializing Airflow database..."
docker-compose exec -T airflow-webserver airflow db init

echo ""
echo "Setup complete!"
echo ""
echo "Services are running:"
echo "   - Airflow UI: http://localhost:8080"
echo "   - PostgreSQL: localhost:5432"
echo ""
echo "Next steps:"
echo "   1. Create Airflow user: make airflow-create-user"
echo "   2. View logs: make logs"
echo "   3. Access shell: make shell"
echo ""
