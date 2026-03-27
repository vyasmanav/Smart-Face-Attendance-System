@echo off
echo ====================================================
echo Starting Smart Face Attendance System Backend...
echo ====================================================

cd /d "%~dp0backend"

if exist "..\.venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "..\.venv\Scripts\activate.bat"
)

echo Starting Django Server on http://127.0.0.1:8000 ...
python manage.py runserver 127.0.0.1:8000
pause
