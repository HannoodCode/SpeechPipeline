#!/bin/bash

# AI Speech Pipeline Frontend Startup Script

echo "🌐 Starting AI Speech Pipeline Frontend..."
export HOST=localhost
export DANGEROUSLY_DISABLE_HOST_CHECK=true
export PORT=3000

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start the development server
echo "🚀 Starting React development server..."
echo "📍 Frontend will be available at: http://localhost:3000"
echo "🔄 Hot reload enabled - changes will be reflected automatically"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo ""

npm start 