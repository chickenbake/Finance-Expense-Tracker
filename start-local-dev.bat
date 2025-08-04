@echo off
echo Setting up Finance Expense Tracker for Local Development...

echo.
echo Starting Backend (Flask API)...
cd "c:\Finance Expense Tracker\backend"
start cmd /k "python app.py"

echo.
echo Starting Frontend (React Development Server)...
cd "c:\Finance Expense Tracker\frontend"
start cmd /k "npm start"

echo.
echo Local development servers started!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul
