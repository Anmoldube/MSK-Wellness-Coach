# Simple dependency installer
Write-Host "Installing dependencies..." -ForegroundColor Green

pip install structlog
pip install sqlalchemy
pip install asyncpg
pip install alembic
pip install chromadb
pip install slowapi
pip install python-multipart
pip install Pillow
pip install aiofiles
pip install python-json-logger

Write-Host "`nDone! Now restart backend with:" -ForegroundColor Green
Write-Host "uvicorn app.main:app --reload --port 8000" -ForegroundColor Cyan
