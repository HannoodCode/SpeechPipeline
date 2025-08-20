#!/bin/bash

echo "🔒 Starting Frontend with HTTPS for microphone access..."
echo "📍 Frontend will be available at: https://localhost:3000"
echo ""

# Start React with HTTPS
HTTPS=true SSL_CRT_FILE=localhost.pem SSL_KEY_FILE=localhost-key.pem npm start 