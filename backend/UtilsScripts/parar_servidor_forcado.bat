@echo off
:: ====================================================
:: PARAR SERVIDOR FORÇADO
:: Mata TODOS os processos na porta 5000
:: ====================================================

title Parar Servidor Forcado

echo.
echo ============================================
echo   PARAR TODOS OS SERVIDORES (FORCADO)
echo ============================================
echo.

echo Procurando processos na porta 5000...
echo.

:: Listar todos os PIDs usando porta 5000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    echo Matando processo PID: %%a
    taskkill /F /PID %%a
)

echo.
echo Matando todos os processos Python...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
taskkill /F /IM py.exe 2>nul

echo.
echo ============================================
echo   VERIFICANDO SE PAROU...
echo ============================================
echo.

timeout /t 2 /nobreak >nul

netstat -ano | findstr :5000 | findstr LISTENING

if %errorlevel% equ 0 (
    echo.
    echo [AVISO] Ainda ha processos na porta 5000!
    echo.
    echo SOLUCAO MANUAL:
    echo 1. Abra Gerenciador de Tarefas (Ctrl+Shift+Esc)
    echo 2. Procure por "Python"
    echo 3. Finalize todos os processos Python
    echo.
    pause
) else (
    echo.
    echo ============================================
    echo   SUCESSO! Porta 5000 esta livre!
    echo ============================================
    echo.
)

pause

