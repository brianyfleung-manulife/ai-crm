#!/bin/bash

echo "🚀 Starting AI CRM Chatbot Development Environment"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

echo "✅ Python and Node.js are installed"

# Check if virtual environment exists for API
if [ ! -d "api/venv" ]; then
    echo "📦 Creating Python virtual environment..."
    cd api && python3 -m venv venv && cd ..
fi

echo "📦 Installing dependencies..."

# Install API dependencies
echo "Installing API dependencies..."
cd api
source venv/bin/activate 2>/dev/null || venv\Scripts\activate
pip install -r requirements.txt
deactivate 2>/dev/null || true
cd ..

# Install App dependencies
echo "Installing App dependencies..."
cd app
npm install
cd ..

echo "✅ All dependencies installed successfully!"
echo ""
echo "To start the development environment:"
echo "1. Backend (with hot reload): cd api && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo "   (Or, for Windows: venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000)"
echo "2. Frontend: cd app && npm run dev"
echo ""
echo "Or use the combined script: npm run dev"
echo ""
echo "🌐 Frontend will be available at: http://localhost:5173"
echo "🔧 Backend API will be available at: http://localhost:8000"
