@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
cls

echo ============================================
echo   Plante Uma Flor v2.0
echo   PREPARAR MIGRAÇÃO DE PASTA
echo ============================================
echo.
echo Este script vai parar TODOS os processos
echo Python para permitir mover o projeto.
echo.
echo ============================================
pause
echo.

echo [1/5] Parando servidor na porta 5000...
echo.

REM Encontrar e parar processo na porta 5000
set PID=
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000" ^| findstr "LISTENING"') do (
    set PID=%%a
)

if defined PID (
    echo     ✓ Processo encontrado (PID: %PID%)
    taskkill /F /PID %PID% >NUL 2>&1
    echo     ✓ Processo parado
) else (
    echo     ℹ Nenhum processo na porta 5000
)

echo.
echo [2/5] Parando TODOS os processos python.exe...
echo.

tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    taskkill /F /IM python.exe >NUL 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo     ✓ Processos python.exe encerrados
    ) else (
        echo     ⚠ Falha ao encerrar python.exe
    )
) else (
    echo     ℹ Nenhum processo python.exe encontrado
)

echo.
echo [3/5] Parando TODOS os processos pythonw.exe (background)...
echo.

tasklist /FI "IMAGENAME eq pythonw.exe" 2>NUL | find /I /N "pythonw.exe">NUL
if "%ERRORLEVEL%"=="0" (
    taskkill /F /IM pythonw.exe >NUL 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo     ✓ Processos pythonw.exe encerrados
    ) else (
        echo     ⚠ Falha ao encerrar pythonw.exe
    )
) else (
    echo     ℹ Nenhum processo pythonw.exe encontrado
)

echo.
echo [4/5] Aguardando liberação de arquivos...
echo.

timeout /t 5 /nobreak >nul
echo     ✓ Aguardado 5 segundos

echo.
echo [5/5] Verificação final...
echo.

REM Verificar se ainda há processos Python
set PYTHON_RUNNING=0
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" set PYTHON_RUNNING=1

tasklist /FI "IMAGENAME eq pythonw.exe" 2>NUL | find /I /N "pythonw.exe">NUL
if "%ERRORLEVEL%"=="0" set PYTHON_RUNNING=1

if %PYTHON_RUNNING% EQU 1 (
    echo     ⚠ AVISO: Ainda há processos Python em execução!
    echo     ⚠ Pode ser necessário reiniciar o computador.
    echo.
    pause
    exit /b 1
) else (
    echo     ✓ Nenhum processo Python em execução
)

REM Verificar porta 5000
netstat -ano | findstr ":5000" | findstr "LISTENING" >NUL 2>&1
if %ERRORLEVEL% EQU 0 (
    echo     ⚠ AVISO: Porta 5000 ainda está em uso!
    echo.
    pause
    exit /b 1
) else (
    echo     ✓ Porta 5000 livre
)

echo.
echo ============================================
echo   ✓ PREPARAÇÃO CONCLUÍDA COM SUCESSO!
echo ============================================
echo.
echo Agora você pode executar MIGRAR_PROJETO.bat
echo para mover o projeto para o novo local.
echo.
echo ============================================
pause

