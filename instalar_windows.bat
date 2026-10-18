@echo off
title Finance - Instalacion
cd /d "%~dp0"
echo Creando entorno virtual (.venv) si no existe...
if not exist ".venv\Scripts\python.exe" python -m venv .venv
echo Instalando dependencias...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if not exist ".env" copy ".env.example" ".env" >nul
echo.
echo Listo. Ahora ejecuta iniciar_web.bat
pause
