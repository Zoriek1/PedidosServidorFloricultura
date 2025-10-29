@echo off
REM ====================================================
REM Plante Uma Flor - PWA v3.0
REM Script para iniciar o servidor Flask em background
REM ====================================================

cd /d "%~dp0"

echo.
echo ====================================================
echo  Plante Uma Flor - PWA v3.0
echo  Iniciando servidor em segundo plano...
echo ====================================================
echo.

REM Verificar se o servidor já está rodando
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *main.py*" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [AVISO] Servidor ja esta em execucao!
    echo.
    pause
    exit /b
)

REM Iniciar o servidor em uma nova janela minimizada
start "Plante Uma Flor - Servidor PWA" /MIN python main.py

echo.
echo [OK] Servidor iniciado com sucesso!
echo.
echo O servidor esta rodando em segundo plano.
echo Para parar o servidor, feche a janela minimizada ou execute: parar_servidor.bat
echo.
echo Acesse o sistema em:
echo   Local:   http://localhost:5000
echo   Rede:    http://192.168.1.148:5000
echo.
timeout /t 5

exit

