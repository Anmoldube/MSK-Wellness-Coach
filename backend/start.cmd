@echo off
echo Starting MSK Wellness Coach Backend with POE API...
echo.
C:\Users\anmol\Desktop\mkl\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
