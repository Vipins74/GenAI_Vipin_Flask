#!/bin/bash

# Lead Scoring System Startup Script

echo "🚀 Starting Lead Scoring System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Start the application
echo "🌟 Starting Flask application..."
echo "📱 Access the application at: http://localhost:5000"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

python app.py