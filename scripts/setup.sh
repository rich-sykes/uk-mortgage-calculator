#!/bin/bash

# Build and run UK Mortgage Calculator for local development

echo "🏠 UK Mortgage Calculator - Local Development Setup"
echo "=================================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is required but not installed."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup API (Azure Functions)
echo "📡 Setting up API..."
cd api

echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "✅ API setup complete"

# Setup Web frontend
echo "🌐 Setting up Web frontend..."
cd ../web

echo "Installing Node.js dependencies..."
npm install

echo "✅ Web frontend setup complete"

# Go back to root
cd ..

echo ""
echo "🎉 Setup complete! To start development:"
echo ""
echo "1. Start the API (Azure Functions):"
echo "   cd api && func start"
echo ""
echo "2. Start the Web frontend (in a new terminal):"
echo "   cd web && npm run dev"
echo ""
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "📚 Documentation:"
echo "   - API docs: http://localhost:7071"
echo "   - Web app: http://localhost:3000"
echo ""
