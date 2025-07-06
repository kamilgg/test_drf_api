#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting Wallet API services...${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Start the services
docker-compose up -d

# Check if services started successfully
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Services started successfully!${NC}"
    echo -e "${GREEN}API is available at:${NC} http://localhost:8000/api/"
    echo -e "${GREEN}API Documentation:${NC}"
    echo -e "  - Swagger UI: http://localhost:8000/api/docs/"
    echo -e "  - ReDoc: http://localhost:8000/api/redoc/"
else
    echo "Failed to start services. Please check the logs with 'docker-compose logs'."
    exit 1
fi

echo -e "\n${YELLOW}To stop the services, run:${NC} docker-compose down"