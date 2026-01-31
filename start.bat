@echo off
REM Startup script for Jordan Vectorizer API (Windows)

echo ==========================================
echo Jordan Vectorizer API - Starting...
echo ==========================================

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Node.js is not installed
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed
    exit /b 1
)

REM Install Node.js dependencies if needed
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call yarn install
)

REM Build native module if needed
if not exist "index.js" (
    echo Building native module...
    call yarn build
)

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r api\requirements.txt

REM Start the API server
echo Starting API server on http://localhost:8000
echo ==========================================
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
