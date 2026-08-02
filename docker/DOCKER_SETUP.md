# Docker Setup Guide

This guide explains how to run the Data Project in Docker.

## Prerequisites

- Docker Desktop (or Docker Engine) installed
- Docker Compose installed
- At least 4GB of RAM allocated to Docker

## Quick Start - Production Environment

### 1. Clone/Setup Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 2. Build Docker Images

```bash
make build
```

Or manually:

```bash
docker-compose build
```

### 3. Start Services

```bash
make up
```

This will start:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Airflow Webserver (port 8080)
- Airflow Scheduler
- Airflow Celery Worker
- FastAPI (port 8000)
- dbt Service

### 4. Initialize Airflow

```bash
docker-compose exec airflow-webserver airflow db init
```

### 5. Create Admin User (Optional)

```bash
docker-compose exec airflow-webserver airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

### 6. Access Services

- **Airflow UI**: http://localhost:8080
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Development Environment

For development with hot-reload and debugging:

```bash
make dev-up
```

This uses `docker-compose.dev.yml` with:
- Volume mounts for live code changes
- Development tools (pytest, black, flake8, etc.)
- Interactive terminal access

```bash
make dev-down
```

## Common Commands

### View Logs

```bash
make logs
# or specific service
docker-compose logs -f airflow-webserver
docker-compose logs -f fastapi-app
```

### Open Shell

```bash
make shell
# or in specific container
docker-compose exec airflow-webserver bash
docker-compose exec fastapi-app bash
```

### Run Tests

```bash
make test
```

### Format Code

```bash
make format
make lint
```

### dbt Commands

```bash
# Run dbt models
make dbt-run

# Test dbt models
make dbt-test

# Generate documentation
make dbt-docs
```

## Stopping Services

```bash
make down
# or with volume cleanup
make clean
```

## Troubleshooting

### PostgreSQL Connection Issues

Check if PostgreSQL is healthy:

```bash
docker-compose ps
```

Verify connection:

```bash
docker-compose exec postgres psql -U airflow -d airflow -c "SELECT 1"
```

### Airflow Won't Start

Check logs:

```bash
docker-compose logs airflow-webserver
```

Reinitialize database:

```bash
docker-compose down -v
docker-compose up -d postgres redis
docker-compose exec airflow-webserver airflow db init
```

### Port Already in Use

Change ports in `docker-compose.yml`:

```yaml
ports:
  - "8081:8080"  # Change 8080 to 8081
```

## Project Structure

```
.
├── Dockerfile              # Production image
├── Dockerfile.dev          # Development image
├── docker-compose.yml      # Production services
├── docker-compose.dev.yml  # Development services
├── .dockerignore           # Files to exclude from build
├── .env.example            # Environment variables template
├── init-db.sql            # Database initialization
├── .dbt/profiles.yml      # dbt configuration
├── Makefile               # Helper commands
└── DOCKER_SETUP.md        # This file
```

## Environment Variables

Key variables in `.env`:

- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: PostgreSQL password
- `DB_NAME`: PostgreSQL database name
- `FERNET_KEY`: Airflow encryption key (generate new for production)
- `API_HOST/PORT`: FastAPI configuration

## Production Considerations

1. **Generate a new FERNET_KEY**:

```bash
docker-compose exec app python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

2. **Use strong passwords** in `.env`

3. **Configure resource limits** in `docker-compose.yml`

4. **Use environment-specific compose files**

5. **Set up logging/monitoring**

6. **Regular database backups**:

```bash
docker-compose exec postgres pg_dump -U airflow airflow > backup.sql
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Apache Airflow Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- [dbt Docker Image](https://hub.docker.com/r/dbt-labs/dbt-postgres)

