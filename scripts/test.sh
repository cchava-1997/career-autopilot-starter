#!/bin/bash

# Career Autopilot Test Runner
# Runs all tests for the application

set -e

echo "🧪 Running Career Autopilot Tests..."

# Activate virtual environment
source .venv/bin/activate

# Run Python tests
echo "🐍 Running Python tests..."
python -m pytest tests/api/ -v --tb=short

# Run frontend tests
echo "⚛️  Running frontend tests..."
cd apps/frontend
npm test -- --coverage --watchAll=false
cd ../..

# Run linting
echo "🔍 Running linting..."
python -m flake8 apps/backend/ --max-line-length=100
cd apps/frontend
npm run lint
cd ../..

echo "✅ All tests passed!"
