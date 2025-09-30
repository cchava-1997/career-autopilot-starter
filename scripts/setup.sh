#!/bin/bash

# Career Autopilot Setup Script
# This script sets up the development environment on macOS

set -e

echo "🚀 Setting up Career Autopilot..."

# Check if Python 3.10+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
if [[ $(echo "$PYTHON_VERSION < 3.10" | bc -l) -eq 1 ]]; then
    echo "❌ Python 3.10+ required. Current version: $PYTHON_VERSION"
    echo "Install via Homebrew: brew install python@3.11"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
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
mkdir -p tests/api
mkdir -p tests/ui
mkdir -p tests/workers
mkdir -p tests/e2e

# Copy environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Install Playwright for autofill
echo "🎭 Installing Playwright..."
pip install playwright
playwright install chromium

# Install LaTeX (BasicTeX)
echo "📄 Installing LaTeX..."
if ! command -v pdflatex &> /dev/null; then
    echo "Installing BasicTeX..."
    brew install --cask basictex
    echo "⚠️  Please restart your terminal and run 'sudo tlmgr update --self' to complete LaTeX setup"
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Start the backend: uvicorn apps.backend.main:app --reload"
echo "3. Start the frontend: cd apps/frontend && npm run dev"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "Happy job hunting! 🎯"
