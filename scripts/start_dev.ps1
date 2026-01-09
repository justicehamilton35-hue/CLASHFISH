# ClashFish Development Startup Script (Windows PowerShell)

Write-Host "🚀 Starting ClashFish in Development Mode" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
if (-not (Test-Path .env)) {
    Write-Host "📝 Creating .env file from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ .env file created. Please configure your API keys if needed." -ForegroundColor Green
    Write-Host ""
}

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "🐍 Python detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.10+ from python.org" -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path venv)) {
    Write-Host "🐍 Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created." -ForegroundColor Green
    Write-Host ""
}

# Activate virtual environment
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
pip install --quiet --upgrade pip
pip install --quiet -r backend\requirements.txt

Write-Host ""
Write-Host "⚠️  Database Check:" -ForegroundColor Yellow
Write-Host "   If you're using mock data (USE_MOCK_DATA=true), you can skip database setup."
Write-Host "   Otherwise, ensure PostgreSQL is running on port 5432."
Write-Host ""

# Start the backend server
Write-Host "🎮 Starting ClashFish Backend..." -ForegroundColor Cyan
Write-Host ""
Write-Host "   API:        http://localhost:8000" -ForegroundColor Green
Write-Host "   Dashboard:  http://localhost:8000" -ForegroundColor Green
Write-Host "   API Docs:   http://localhost:8000/docs" -ForegroundColor Green
Write-Host "   Health:     http://localhost:8000/api/v1/health" -ForegroundColor Green
Write-Host ""

# Check if using mock data
$envContent = Get-Content .env -Raw
if ($envContent -match 'USE_MOCK_DATA=true') {
    Write-Host "📊 Mock Data Mode: ENABLED (using sample data)" -ForegroundColor Yellow
} else {
    Write-Host "📊 Real API Mode: ENABLED (using Clash Royale API)" -ForegroundColor Green
}

Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Change to backend directory and run uvicorn
Set-Location backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
