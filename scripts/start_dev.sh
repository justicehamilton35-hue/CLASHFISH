#!/bin/bash

# ClashFish Development Startup Script

echo "🚀 Starting ClashFish in Development Mode"
echo "=========================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please configure your API keys if needed."
fi

# Check if Python virtual environment exists
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created."
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r backend/requirements.txt

# Check if PostgreSQL is running (optional - only if not using mock data)
echo ""
echo "⚠️  Database Check:"
echo "   If you're using mock data (USE_MOCK_DATA=true), you can skip database setup."
echo "   Otherwise, ensure PostgreSQL is running on port 5432."
echo ""

# Start the backend server
echo "🎮 Starting ClashFish Backend..."
echo ""
echo "   API:        http://localhost:8000"
echo "   Dashboard:  http://localhost:8000"
echo "   API Docs:   http://localhost:8000/docs"
echo "   Health:     http://localhost:8000/api/v1/health"
echo ""
echo "📊 Mock Data Mode: ENABLED (using sample data)"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Run the application
cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
