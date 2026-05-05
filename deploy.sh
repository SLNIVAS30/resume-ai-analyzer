#!/bin/bash

# Resume AI Analyzer - Deployment Script

echo "🚀 Starting Resume AI Analyzer Deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p Uploaded_Resumes
mkdir -p ssl

# Build and run the application
echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting application..."
docker-compose up -d

# Wait for application to start
echo "⏳ Waiting for application to start..."
sleep 10

# Check if application is running
if curl -f http://localhost:8501/_stcore/health &> /dev/null; then
    echo "✅ Application is running successfully!"
    echo "🌐 Access the application at: http://localhost"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs"
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo "📋 Useful commands:"
echo "  View logs: docker-compose logs -f"
echo "  Stop app: docker-compose down"
echo "  Restart: docker-compose restart"
