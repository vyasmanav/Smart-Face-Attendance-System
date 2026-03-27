# Smart Face Attendance System - Environment Setup Script
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " Setting up Smart Face Attendance System Environment" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

# 1. Check Python version
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH." -ForegroundColor Red
    Exit 1
}

# 2. Virtual Environment
if (-not (Test-Path ".venv")) {
    Write-Host "[INFO] Creating virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv .venv
} else {
    Write-Host "[OK] Virtual environment already exists." -ForegroundColor Green
}

# 3. Install requirements
Write-Host "[INFO] Installing Python dependencies..." -ForegroundColor Yellow
& .\.venv\Scripts\pip install --upgrade pip
& .\.venv\Scripts\pip install -r requirements.txt

# 4. Check Environment File
if (-not (Test-Path "backend\.env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" "backend\.env"
        Write-Host "[INFO] Created backend/.env from .env.example template." -ForegroundColor Yellow
    }
}

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " Setup complete! Run .\run_backend.bat to start." -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Cyan
