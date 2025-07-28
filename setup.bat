@echo off
echo Setting up Personal Expense Tracker...
echo.

echo Step 1: Setting up Python backend...
cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Step 2: Setting up React frontend...
cd ..\frontend

echo Installing Node.js dependencies...
npm install

echo.
echo Setup complete!
echo.
echo To start the application:
echo 1. Backend: cd backend && venv\Scripts\activate && python app.py
echo 2. Frontend: cd frontend && npm start
echo.
echo Backend will run on: http://localhost:5000
echo Frontend will run on: http://localhost:3000
echo.
pause
