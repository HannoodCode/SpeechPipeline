#!/bin/bash

# AI Speech Pipeline - Master Startup Script

echo "AI Speech Pipeline - Portfolio Project"
echo "========================================"
echo ""

# Function to run backend
start_backend() {
    echo "Starting Backend..."
    cd backend
    chmod +x start.sh
    ./start.sh &
    BACKEND_PID=$!
    cd ..
}

# Function to run frontend
start_frontend() {
    echo "Starting Frontend..."
    cd frontend
    chmod +x start.sh
    ./start.sh &
    FRONTEND_PID=$!
    cd ..
}

# Function to cleanup processes
cleanup() {
    echo ""
    echo "Shutting down..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    exit 0
}

# Trap interrupt signal
trap cleanup INT

echo "Starting both backend and frontend..."
echo ""

# Start backend
start_backend

# Wait a moment for backend to start
sleep 3

# Start frontend
start_frontend

echo ""
echo "Both services are starting up..."
echo ""
echo "Backend API: http://localhost:8000"
echo "Frontend UI: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Make sure you've configured your API keys in backend/.env"
echo "See README.md for detailed setup instructions"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for both processes
wait 