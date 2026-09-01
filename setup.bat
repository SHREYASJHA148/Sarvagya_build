@echo off
REM Sarvagya Full-Stack Setup Script for Windows

setlocal enabledelayedexpansion

cls
echo ========================================
echo Sarvagya - AI Trading Chart Analysis
echo Full-Stack Setup
echo ========================================
echo.

REM Check if API key is set
if not defined GOOGLE_API_KEY (
    echo [WARNING] GOOGLE_API_KEY not set in environment
    echo Set it with: set GOOGLE_API_KEY=your-api-key
    echo Or create a .env file in the backend directory with:
    echo   GOOGLE_API_KEY=your-api-key
    echo.
)

REM Backend setup
echo [1/2] Setting up backend...
cd backend

if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

echo Installing backend dependencies...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt

echo [OK] Backend ready
echo.

REM Frontend setup
echo [2/2] Setting up frontend...
cd ..\frontend

if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install -q
)

echo [OK] Frontend ready
echo.

REM Instructions
echo ========================================
echo Setup Complete!
echo ========================================
echo.

echo To run Sarvagya:
echo.
echo [Terminal 1 - Backend]
echo   cd backend
echo   set GOOGLE_API_KEY=your-api-key
echo   venv\Scripts\activate.bat
echo   python main.py
echo.

echo [Terminal 2 - Frontend]
echo   cd frontend
echo   npm run dev
echo.

echo Then open http://localhost:3000 in your browser
