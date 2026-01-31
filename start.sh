#!/bin/bash

# Startup script for Jordan Vectorizer API

echo "=========================================="
echo "Jordan Vectorizer API - Starting..."
echo "=========================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Install Node.js dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    yarn install
fi

# Build native module if needed
if [ ! -f "index.js" ]; then
    echo "Building native module..."
    yarn build
fi

# Install Python dependencies if needed
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "Installing Python dependencies..."
    pip3 install -r api/requirements.txt
fi

# Start the API server
echo "Starting API server on http://0.0.0.0:8000"
echo "=========================================="
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000
