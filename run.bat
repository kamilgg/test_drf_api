@echo off
echo Starting Wallet API services...

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Docker is not installed. Please install Docker first.
    exit /b 1
)

REM Check if Docker Compose is installed
where docker-compose >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

REM Start the services
docker-compose up -d

REM Check if services started successfully
if %ERRORLEVEL% equ 0 (
    echo Services started successfully!
    echo API is available at: http://localhost:8000/api/
    echo API Documentation:
    echo   - Swagger UI: http://localhost:8000/api/docs/
    echo   - ReDoc: http://localhost:8000/api/redoc/
) else (
    echo Failed to start services. Please check the logs with 'docker-compose logs'.
    exit /b 1
)

echo.
echo To stop the services, run: docker-compose down