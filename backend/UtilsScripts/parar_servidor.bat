@echo off
:: ====================================================
:: Plante Uma Flor - PWA v3.0
:: Script para PARAR o servidor Flask
:: ====================================================

title Parar Servidor - Plante Uma Flor

echo.
echo ====================================================
echo  Plante Uma Flor - PWA v3.0
echo  Parando TODOS os servidores...
echo ====================================================
echo.

:: Método 1: Parar processo usando porta 5000
echo [1/3] Verificando porta 5000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    echo Matando processo usando porta 5000 (PID: %%a)
    taskkill /F /PID %%a >nul 2>&1
)

:: Método 2: Matar todos os processos python.exe
echo [2/3] Parando processos Python...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1

:: Método 3: Matar processos py.exe
echo [3/3] Parando processos Py Launcher...
taskkill /F /IM py.exe >nul 2>&1

echo.
echo ============================================
echo   SERVIDORES PARADOS!
echo ============================================
echo.
echo Todos os processos Python foram encerrados.
echo A porta 5000 esta livre.
echo.
echo Agora voce pode iniciar o servidor novamente:
echo   - HTTP: python main.py
echo   - HTTPS: python main.py --https
echo.
echo ============================================
echo.
timeout /t 3

exit

