@echo off
echo Starting ITSD Admin Copilot Backend...
echo.

cd backend
echo Installing Python dependencies...
pip install -r requirements.txt

echo Starting Flask server...
python run.py

pause