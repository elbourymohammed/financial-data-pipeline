# Docker & Kubernetes Configuration Files

This directory contains Docker and Kubernetes deployment configurations.

## Files Overview

### Docker Production Setup
- **Dockerfile** - Production Docker image for the application
- **docker-compose.yml** - Complete production environment with all services
- **.dockerignore** - Files to exclude from Docker builds

### Docker Development Setup
- **Dockerfile.dev** - Development image with testing/debugging tools
- **docker-compose.dev.yml** - Development environment (simplified)
- **docker-compose.override.yml** - Local overrides for development

### Configuration & Initialization
- **.env.example** - Environment variables template
- **init-db.sql** - PostgreSQL database initialization script
- **.dbt/profiles.yml** - dbt profiles configuration

### Helper Scripts & Documentation
- **docker-init.sh** - Quick setup script for first-time initialization
- **docker-helper.sh** - Helper commands for Docker operations
- **Makefile** - Make commands for common operations
- **DOCKER_SETUP.md** - Complete Docker setup guide

## Quick Start

### First-time Setup
```bash
bash docker-init.sh
```

### Daily Development
```bash
# Start services
make dev-up

# View logs
make logs

# Open shell
make shell

# Run tests
make test

# Stop services
make dev-down
```

### Production Deployment
```bash
# Build production images
make build

# Start all services
make up

# Create admin user
make airflow-create-user

# Stop services
make down
```

## Service Architecture

```
┌─────────────────────────────────────────┐
│       Docker Compose Network            │
├─────────────────────────────────────────┤
│  PostgreSQL (5432)                      │
│  ├─ Airflow Metadata DB                 │
│  └─ Application Data                    │
├─────────────────────────────────────────┤
│  Redis (6379)                           │
│  └─ Celery Message Broker               │
├─────────────────────────────────────────┤
│  Airflow (8080)                         │
│  ├─ Webserver                           │
│  ├─ Scheduler                           │
│  └─ Celery Worker                       │
├─────────────────────────────────────────┤
│  FastAPI (8000)                         │
│  └─ REST API Application                │
├─────────────────────────────────────────┤
│  dbt (Container)                        │
│  └─ Data Transformations                │
└─────────────────────────────────────────┘
```

## Environment Variables

Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

Key variables:
- `DB_USER` - PostgreSQL username
- `DB_PASSWORD` - PostgreSQL password
- `FERNET_KEY` - Airflow encryption key
- `API_HOST/PORT` - API configuration

## Common Issues & Solutions

### Cannot connect to PostgreSQL
```bash
make health
docker-compose logs postgres
```

### Airflow won't initialize
```bash
docker-compose down -v
docker-compose up -d postgres
```

### Port conflicts
Edit `docker-compose.yml` and change port mappings

### Out of disk space
```bash
make clean
```

## Useful Commands

```bash
# View status
make dev-up
make logs

# Access databases
make shell
docker-compose exec postgres psql -U airflow

# Run tests
make test

# Format and lint
make format
make lint

# dbt commands
make dbt-run
make dbt-test
```

## For More Information

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for detailed instructions.
