# Start Backend Server
# This script starts the FastAPI backend server

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Backend Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to backend directory
Set-Location backend

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "✗ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Check for API key
if (-not $env:OPENAI_API_KEY) {
    Write-Host "⚠ Warning: OPENAI_API_KEY not set!" -ForegroundColor Yellow
    Write-Host ""
    $apiKey = Read-Host "Enter your OpenAI API Key (or press Enter to skip)"
    if ($apiKey) {
        $env:OPENAI_API_KEY = $apiKey
        Write-Host "✓ API key set for this session" -ForegroundColor Green
    }
    Write-Host ""
}

# Start the server
Write-Host "Starting FastAPI server on http://localhost:8000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python app.py
