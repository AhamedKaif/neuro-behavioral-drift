@echo off
echo ============================================
echo  Neuro-Behavioral Drift - Setup Script
echo ============================================
echo.

REM 1. Train ML Model
echo [1/3] Training ML Model...
cd ml-model
python generate_dataset.py
python train.py
cd ..
echo ML Model trained successfully.
echo.

REM 2. Initialize Database
echo [2/3] Initializing Database...
cd backend
python db.py
cd ..
echo Database initialized.
echo.

REM 3. Install Frontend Dependencies
echo [3/3] Installing Frontend Dependencies...
cd frontend
call npm install
cd ..
echo Frontend dependencies installed.
echo.

echo ============================================
echo  Setup Complete!
echo ============================================
echo.
echo To run the application:
echo.
echo   Terminal 1 (Backend):
echo     cd backend
echo     python app.py
echo.
echo   Terminal 2 (Frontend):
echo     cd frontend
echo     npm run dev
echo.
echo   Then open http://localhost:5173
echo ============================================
