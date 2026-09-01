@echo off
REM Sarvagya_robust - Safer one-click launcher (no embedded API key)

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
set "BACKEND_DIR=%SCRIPT_DIR%backend"
set "FRONTEND_DIR=%SCRIPT_DIR%frontend"
set "BACKEND_PY=%BACKEND_DIR%\venv\Scripts\python.exe"

REM Load GOOGLE_API_KEY from backend/.env (if present)
if exist "%BACKEND_DIR%\.env" (
  for /f "usebackq tokens=1,* delims==" %%a in ("%BACKEND_DIR%\.env") do (
    if /i "%%a"=="GOOGLE_API_KEY" (
      set "GOOGLE_API_KEY=%%b"
    )
  )
)

echo ================================================================
echo                        SARVAGYA LAUNCHER
echo              AI Trading Chart Analysis Platform
echo ================================================================
echo.
echo Backend:   http://localhost:8000
echo Frontend:  http://localhost:3000
echo.

if not exist "%BACKEND_DIR%" (
  echo ERROR: Backend folder not found: "%BACKEND_DIR%"
  exit /b 1
)
if not exist "%BACKEND_PY%" (
  echo ERROR: Backend venv python not found: "%BACKEND_PY%"
  echo Please run setup.bat first.
  exit /b 1
)
if not exist "%FRONTEND_DIR%" (
  echo ERROR: Frontend folder not found: "%FRONTEND_DIR%"
  exit /b 1
)

echo.
echo [1/2] Starting backend...
start "Sarvagya Backend" cmd /k "cd /d \"%BACKEND_DIR%\" && \"%BACKEND_PY%\" main.py"

echo Waiting for backend to initialize (10 seconds)...
timeout /t 10 /nobreak >nul

echo.
echo [2/2] Starting frontend...
start "Sarvagya Frontend" cmd /k "cd /d \"%FRONTEND_DIR%\" && npm run dev"

echo Waiting for frontend to initialize (15 seconds)...
timeout /t 15 /nobreak >nul

echo.
echo Opening browser to http://localhost:3000...
start "" http://localhost:3000

echo.
echo Done. If the app shows backend offline, open the backend terminal window and check for errors.
pause
