@echo off
title Finance - Interfaz web
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Primero ejecuta instalar_windows.bat
  pause
  exit /b 1
)
start "" http://127.0.0.1:5000
".venv\Scripts\python.exe" web_app.py
pause
