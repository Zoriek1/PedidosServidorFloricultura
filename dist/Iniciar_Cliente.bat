@echo off
title Plante Uma Flor v2.0 - Cliente
cls
echo ========================================
echo   PLANTE UMA FLOR V2.0 - CLIENTE
echo ========================================
echo.
echo Iniciando aplicativo...
echo.

REM Executar aplicativo
PlanteUmaFlor-Client.exe

REM Verificar se houve erro
if errorlevel 1 (
    echo.
    echo ========================================
    echo   ERRO AO INICIAR APLICATIVO
    echo ========================================
    echo.
    echo Possiveis causas:
    echo - Servidor nao esta rodando
    echo - Arquivo corrompido
    echo - Falta de permissoes
    echo.
    pause
) else (
    echo.
    echo Aplicativo finalizado normalmente.
)
