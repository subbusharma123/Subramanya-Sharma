@echo off
:: PAIOS Auto-Start Script
:: This runs silently on Windows startup

cd /d "%~dp0"

if not exist "logs" mkdir "logs"

:: Start Streamlit using the venv Python directly (avoids activate/batch-file issues)
start "PAIOS" /min cmd /c ""%~dp0venv\Scripts\python.exe" -m streamlit run "%~dp0dashboard\app.py" --server.headless true --server.port 8501 > "%~dp0logs\dashboard.log" 2>&1"

:: Wait 8 seconds then open dashboard in browser
timeout /t 8 /nobreak >nul
start http://localhost:8501
