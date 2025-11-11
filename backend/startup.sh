#!/bin/bash
# Azure App Service Startup Script for Python
# This script is executed when the container starts

set -e  # Exit on error

echo "========================================="
echo "Starting Azure App Service Initialization"
echo "========================================="

# Print environment info
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"
echo "Current directory: $(pwd)"
echo "Environment: ${ENVIRONMENT:-development}"

# Create necessary directories
mkdir -p /home/site/wwwroot/knowledge_base
mkdir -p /home/site/wwwroot/logs

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "Installing Python dependencies..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt --no-cache-dir
    echo "✓ Dependencies installed successfully"
else
    echo "⚠ requirements.txt not found"
fi

# Check if Azure OpenAI credentials are configured
if [ -z "$AZURE_OPENAI_API_KEY" ]; then
    echo "⚠ WARNING: AZURE_OPENAI_API_KEY not set"
fi

if [ -z "$AZURE_OPENAI_ENDPOINT" ]; then
    echo "⚠ WARNING: AZURE_OPENAI_ENDPOINT not set"
fi

# Get PORT from environment or default to 8000
PORT=${PORT:-8000}
HOST=${HOST:-0.0.0.0}

echo "========================================="
echo "Starting Application"
echo "Host: $HOST"
echo "Port: $PORT"
echo "========================================="

# Start the application using gunicorn for production
# gunicorn is more robust for production than uvicorn alone
if [ "$ENVIRONMENT" = "production" ]; then
    echo "Starting with Gunicorn (production mode)..."
    exec gunicorn app:app \
        --worker-class uvicorn.workers.UvicornWorker \
        --workers 2 \
        --threads 4 \
        --timeout 120 \
        --bind $HOST:$PORT \
        --access-logfile - \
        --error-logfile - \
        --log-level info \
        --preload
else
    echo "Starting with Uvicorn (development mode)..."
    exec python -m uvicorn app:app \
        --host $HOST \
        --port $PORT \
        --log-level info
fi
