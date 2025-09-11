@echo off
echo Setting up Personal Expense Tracker (PET) for Local Development...

echo.
echo Starting Backend (Flask API)...
cd "C:\Users\sol46ex\Porsche Projects\Finance Expense Tracker\backend"
call venv\Scripts\activate
#call source venv/bin/activate  # For Git Bash or WSL
start cmd /k "python app.py"

echo.
echo Starting Frontend (React Development Server)...
cd "C:\Users\sol46ex\Porsche Projects\Finance Expense Tracker\frontend"
start cmd /k "npm start"

echo.
echo Local development servers started!
echo Backend: http://localhost:5001
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul
