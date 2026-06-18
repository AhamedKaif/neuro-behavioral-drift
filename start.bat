@echo off
echo ============================================
echo   Neuro-Behavioral Drift - Start App
echo ============================================
echo.
echo Starting Flask Backend...
start "Neuro-Behavioral Drift Backend" cmd /k "cd backend && python app.py"

echo Starting React Frontend...
start "Neuro-Behavioral Drift Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ============================================
echo Servers are starting in separate windows!
echo.
echo 1. Wait a few seconds for them to boot up.
echo 2. Open your browser and go to: http://localhost:5173
echo.
echo To stop the servers, just close the two command windows.
echo ============================================
pause
