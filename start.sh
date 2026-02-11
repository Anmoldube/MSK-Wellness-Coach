#!/bin/bash

echo "🚀 Starting MSK Wellness AI Chatbot"
echo "===================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "✅ .env file created"
fi

echo "📦 Starting services with Docker Compose..."
echo ""

# Start services
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo ""
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "=================================="
echo "✅ Services Started!"
echo "=================================="
echo ""
echo "🌐 Access points:"
echo "   • Frontend:  http://localhost:5173"
echo "   • Backend:   http://localhost:8000"
echo "   • API Docs:  http://localhost:8000/docs"
echo ""
echo "📋 Useful commands:"
echo "   • View logs:     docker-compose logs -f"
echo "   • Stop services: docker-compose down"
echo "   • Restart:       docker-compose restart"
echo ""
echo "🎉 Ready to use! Open http://localhost:5173 in your browser"
