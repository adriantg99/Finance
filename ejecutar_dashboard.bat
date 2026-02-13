@echo off
title Analizador de Acciones - Dashboard
color 0B

echo.
echo ========================================================================
echo                    ANALIZADOR DE ACCIONES - DASHBOARD
echo ========================================================================
echo.
echo Ejecutando dashboard completo (esto puede tardar 3-5 minutos)...
echo.

cd /d "C:\laragon\www\Finance"
C:\laragon\www\scripts\.venv\Scripts\python.exe dashboard.py

echo.
echo ========================================================================
echo                    DASHBOARD COMPLETADO
echo ========================================================================
echo.

pause
