@echo off
:: ===================================================
:: PLANTE UMA FLOR - Parar Servidor HTTPS
:: Para o servidor Flask HTTPS rodando em background
:: ===================================================

title Parar Servidor HTTPS - Plante Uma Flor

echo.
echo ============================================
echo   PARAR SERVIDOR HTTPS
echo ============================================
echo.

:: Procurar processos Python rodando main.py --https
echo Procurando servidor HTTPS...
echo.

:: Tentar matar processos pela porta 5000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
    taskkill /PID %%a /F >nul 2>&1
)

:: Tentar matar processos Python com main.py
wmic process where "commandline like '%%main.py%%--https%%'" delete >nul 2>&1

:: Verificar se ainda está rodando
timeout /t 1 >nul

netstat -ano | findstr :5000 >nul 2>&1
if %errorlevel% equ 0 (
    echo [AVISO] Servidor ainda pode estar rodando.
    echo.
    echo Execute: parar_servidor_forcado.bat
) else (
    echo [OK] Servidor HTTPS parado!
)

echo.
pause

