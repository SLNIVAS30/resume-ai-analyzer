@echo off
REM Resume AI Analyzer - Windows Deployment Script

echo 🚀 Starting Resume AI Analyzer Deployment...

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker for Windows first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Create necessary directories
echo 📁 Creating directories...
if not exist "Uploaded_Resumes" mkdir "Uploaded_Resumes"
if not exist "ssl" mkdir "ssl"

REM Build and run the application
echo 🔨 Building Docker image...
docker-compose build

echo 🚀 Starting application...
docker-compose up -d

REM Wait for application to start
echo ⏳ Waiting for application to start...
timeout /t 10 /nobreak >nul

REM Check if application is running
curl -f http://localhost:8501/_stcore/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Application is running successfully!
    echo 🌐 Access the application at: http://localhost
) else (
    echo ❌ Application failed to start. Check logs with: docker-compose logs
    pause
    exit /b 1
)

echo 🎉 Deployment completed successfully!
echo 📋 Useful commands:
echo   View logs: docker-compose logs -f
echo   Stop app: docker-compose down
echo   Restart: docker-compose restart
pause
