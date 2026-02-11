# Start Backend Server with Virtual Environment
Write-Host "Starting MSK Wellness Coach Backend with POE API..." -ForegroundColor Green
Write-Host ""

# Navigate to backend directory
Set-Location -Path "backend"

# Start uvicorn with venv Python directly
Write-Host "Starting uvicorn server with POE API enabled..." -ForegroundColor Yellow
Write-Host ""
C:\Users\anmol\Desktop\mkl\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
