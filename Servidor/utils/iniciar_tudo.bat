@echo off
title Gerador de Pedidos - Plante Uma Flor
color 0A

echo ================================================
echo   Gerador de Pedidos - Plante Uma Flor
echo ================================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Instale Python de: https://www.python.org
    pause
    exit /b 1
)

echo Iniciando sistema...
echo.
echo IMPORTANTE: Mantenha esta janela aberta!
echo.
python Gerador_De_Pedidos.py

pause

