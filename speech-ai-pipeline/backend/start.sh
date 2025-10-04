#!/bin/bash

# AI Speech Pipeline Backend Startup Script

echo "Starting AI Speech Pipeline Backend..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
uv pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ".env file not found. Copying from env.example..."
    cp env.example .env
    echo "Please edit .env with your API keys before running the server."
    echo "See README.md for setup instructions."
    exit 1
fi

# Start the server
echo "Starting FastAPI server..."
echo "Backend will be available at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 