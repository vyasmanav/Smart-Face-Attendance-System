@echo off
echo ====================================================
echo Starting Smart Face Attendance System Frontend...
echo ====================================================

cd /d "%~dp0attendance-system-frontend"

echo Serving frontend on http://localhost:5500 ...
start http://localhost:5500/login.html
python -m http.server 5500
pause
