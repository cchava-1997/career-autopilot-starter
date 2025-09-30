#!/bin/bash

# Career Autopilot Development Script
# Runs both backend and frontend together without Docker

set -e

echo "🚀 Starting Career Autopilot Development Environment..."

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd apps/frontend
npm install
cd ../..

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/applications
mkdir -p data/resumes
mkdir -p apps/backend/logs

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend
echo "🔧 Starting backend server..."
source .venv/bin/activate
uvicorn apps.backend.main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is running
if ! curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "❌ Backend failed to start"
    cleanup
    exit 1
fi

echo "✅ Backend is running on http://localhost:8000"

# Start frontend
echo "🔧 Starting frontend server..."
cd apps/frontend
npm run dev &
FRONTEND_PID=$!
cd ../..

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 10

# Check if frontend is running
if ! curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "❌ Frontend failed to start"
    cleanup
    exit 1
fi

echo "✅ Frontend is running on http://localhost:3000"

echo ""
echo "🎉 Career Autopilot is running!"
echo ""
echo "Services:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for user to stop
wait
