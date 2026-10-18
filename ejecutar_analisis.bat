@echo off
title Analizador de Acciones - Analisis Rapido
color 0A

echo.
echo ========================================================================
echo                    ANALIZADOR DE ACCIONES
echo ========================================================================
echo.
echo Ejecutando analisis rapido...
echo.

cd /d "%~dp0"
".venv\Scripts\python.exe" buscar_acciones.py

echo.
echo ========================================================================
echo                    ANALISIS COMPLETADO
echo ========================================================================
echo.

pause
