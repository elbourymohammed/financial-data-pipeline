#!/bin/bash
# Helper script to manage Docker containers

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_info() {
    echo -e "${YELLOW}$1${NC}"
}

case "$1" in
    status)
        print_header "Docker Services Status"
        docker-compose ps
        ;;
    
    logs)
        print_header "Container Logs"
        docker-compose logs -f "${2:-airflow-webserver}"
        ;;
    
    shell)
        SERVICE="${2:-airflow-webserver}"
        print_info "Opening shell in $SERVICE container..."
        docker-compose exec "$SERVICE" bash
        ;;
    
    psql)
        print_info "Connecting to PostgreSQL..."
        docker-compose exec postgres psql -U airflow -d airflow
        ;;
    
    airflow-webui)
        print_info "Opening Airflow Web UI..."
        open http://localhost:8080
        ;;
    
    restart)
        SERVICE="${2:-all}"
        print_header "Restarting $SERVICE"
        docker-compose restart "$SERVICE"
        print_success "Service restarted"
        ;;
    
    rebuild)
        SERVICE="${2:-.}"
        print_header "Rebuilding $SERVICE"
        docker-compose build "$SERVICE"
        print_success "Build complete"
        ;;
    
    health)
        print_header "Health Check"
        echo "PostgreSQL:"
        docker-compose exec -T postgres pg_isready -U airflow
        echo ""
        echo "Redis:"
        docker-compose exec -T redis redis-cli ping
        ;;
    
    dbt-run)
        print_header "Running dbt models"
        docker-compose exec dbt dbt run
        ;;
    
    dbt-test)
        print_header "Testing dbt models"
        docker-compose exec dbt dbt test
        ;;
    
    *)
        echo "Docker Helper Script"
        echo ""
        echo "Usage: $0 {command} [argument]"
        echo ""
        echo "Commands:"
        echo "  status              - Show Docker services status"
        echo "  logs [service]      - View service logs"
        echo "  shell [service]     - Open shell in container"
        echo "  psql                - Connect to PostgreSQL"
        echo "  airflow-webui       - Open Airflow UI in browser"
        echo "  restart [service]   - Restart service(s)"
        echo "  rebuild [service]   - Rebuild Docker image(s)"
        echo "  health              - Check services health"
        echo "  dbt-run             - Run dbt models"
        echo "  dbt-test            - Test dbt models"
        echo ""
        echo "Examples:"
        echo "  $0 logs airflow-webserver"
        echo "  $0 shell airflow-webserver"
        echo "  $0 status"
        ;;
esac
