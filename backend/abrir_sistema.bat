@echo off
REM ====================================================
REM Plante Uma Flor - PWA v3.0
REM Inicia o servidor e abre o navegador automaticamente
REM ====================================================

cd /d "%~dp0"

echo.
echo ====================================================
echo  Plante Uma Flor - PWA v3.0
echo  Inicializando sistema...
echo ====================================================
echo.

REM Verificar se o servidor já está rodando
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *main.py*" 2>NUL | find /I /N "python.exe">NUL

if "%ERRORLEVEL%"=="0" (
    echo [INFO] Servidor ja esta em execucao!
) else (
    echo [INFO] Iniciando servidor em segundo plano...
    start "Plante Uma Flor - Servidor PWA" /MIN python main.py
    echo [OK] Servidor iniciado!
    
    echo [INFO] Aguardando servidor inicializar...
    timeout /t 3 >nul
)

echo [INFO] Abrindo navegador...
start http://localhost:5000

echo.
echo ====================================================
echo  Sistema aberto no navegador!
echo ====================================================
echo.
echo Para parar o servidor, execute: parar_servidor.bat
echo.
timeout /t 3

exit

