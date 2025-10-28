@echo off
chcp 65001 >nul 2>&1
cls

echo ============================================
echo   Plante Uma Flor v2.0 - Parar Servidor
echo ============================================
echo.
echo Procurando servidor na porta 5000...
echo.

REM Encontrar PID do processo usando a porta 5000
set PID=
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000" ^| findstr "LISTENING"') do (
    set PID=%%a
)

if defined PID (
    echo [ENCONTRADO] Servidor rodando com PID: %PID%
    echo Parando servidor...
    taskkill /F /PID %PID% >NUL 2>&1
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo [OK] Servidor parado com sucesso!
    ) else (
        echo.
        echo [ERRO] Falha ao parar o servidor.
    )
) else (
    echo [AVISO] Nenhum servidor encontrado na porta 5000.
    echo.
    echo Tentando parar todos os processos Python...
    
    tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
    if "%ERRORLEVEL%"=="0" (
        taskkill /F /IM python.exe >NUL 2>&1
        echo [OK] Processos Python encerrados.
    ) else (
        echo [AVISO] Nenhum processo Python encontrado.
    )
    
    tasklist /FI "IMAGENAME eq pythonw.exe" 2>NUL | find /I /N "pythonw.exe">NUL
    if "%ERRORLEVEL%"=="0" (
        taskkill /F /IM pythonw.exe >NUL 2>&1
        echo [OK] Processos pythonw encerrados.
    )
)

echo.
echo ============================================
pause


