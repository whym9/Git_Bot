#!/bin/bash
# Build the Docker containers
docker-compose build

# Start the containers (in detached mode)
docker-compose up -d
