#!/bin/bash

# Stop existing containers
docker-compose down

# Build and start containers
docker-compose up -d --build

# Show logs
docker-compose logs -f
