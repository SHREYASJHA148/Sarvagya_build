@echo off
REM Sarvagya - One-Click Launcher for Windows
REM This script starts both backend and frontend in separate windows

setlocal enabledelayedexpansion

REM Set API key
set GOOGLE_API_KEY=YOUR_GEMINI_API_KEY

cls
echo ================================================================
echo                        SARVAGYA LAUNCHER
echo              AI Trading Chart Analysis Platform
echo ================================================================
echo.
echo Starting Sarvagya Backend and Frontend...
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Two terminal windows will open:
echo   1. Backend (Python/FastAPI) - DO NOT CLOSE
echo   2. Frontend (React/Vite) - DO NOT CLOSE
echo.
echo Wait for both to finish starting...
echo Then your browser will automatically open to the chat interface.
echo.
echo ================================================================
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Check if backend venv exists
if not exist "%SCRIPT_DIR%backend\venv" (
    echo ERROR: Python virtual environment not found!
    echo.
    echo Please run setup.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist "%SCRIPT_DIR%frontend\node_modules" (
    echo ERROR: Node.js dependencies not found!
    echo.
    echo Please run setup.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

REM Kill any existing services on ports 8000 and 3000 (optional cleanup)
echo Checking for existing services...
netstat -ano | findstr ":8000" >nul && (
    echo Existing service on port 8000 found. Stopping it...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do taskkill /PID %%a /F 2>nul
    timeout /t 2 /nobreak >nul
)

netstat -ano | findstr ":3000" >nul && (
    echo Existing service on port 3000 found. Stopping it...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3000"') do taskkill /PID %%a /F 2>nul
    timeout /t 2 /nobreak >nul
)

REM Start Backend in new window
echo.
echo [1/2] Starting Backend on localhost:8000...
start "Sarvagya Backend" cmd /k "cd /d ""%SCRIPT_DIR%backend"" && call ""%SCRIPT_DIR%backend\venv\Scripts\activate.bat"" && python ""%SCRIPT_DIR%backend\main.py"""

REM Wait for backend to fully start
echo Waiting for backend to initialize (10 seconds)...
timeout /t 10 /nobreak >nul

REM Start Frontend in new window
echo [2/2] Starting Frontend on localhost:3000...
start "Sarvagya Frontend" cmd /k "cd /d ""%SCRIPT_DIR%frontend"" && npm run dev"

REM Wait for frontend to be ready
echo Waiting for frontend to initialize (15 seconds)...
timeout /t 15 /nobreak >nul

REM Verify both services are running
echo.
echo Verifying services...

REM Check backend
netstat -ano | findstr ":8000" >nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Backend is running on localhost:8000
) else (
    echo [WARNING] Backend may not be running yet
    echo          Check the Backend terminal window
)

REM Check frontend
netstat -ano | findstr ":3000" >nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Frontend is running on localhost:3000
) else (
    echo [WARNING] Frontend may not be running yet
    echo          Check the Frontend terminal window
)

echo.
echo Opening browser to http://localhost:3000...
start http://localhost:3000

echo.
echo ================================================================
echo.
echo Sarvagya is starting!
echo.
echo Check the two terminal windows for startup messages:
echo.
echo BACKEND:
echo   Should show: "INFO:     Uvicorn running on http://0.0.0.0:8000"
echo.
echo FRONTEND:
echo   Should show: "Local:   http://localhost:3000/"
echo.
echo Once both show they're running, your browser will display
echo the Sarvagya chat interface.
echo.
echo IF BROWSER DOESN'T OPEN:
echo   Manually open: http://localhost:3000
echo.
echo TO STOP SARVAGYA:
echo   Close both terminal windows (Backend and Frontend)
echo.
echo ================================================================
echo.
echo Setup complete! Browser opening in 3 seconds...
timeout /t 3 /nobreak >nul

echo.
echo This launcher window can be closed - both services will
echo continue running in their own windows.
echo.
pause
