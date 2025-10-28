@echo off
chcp 65001 >nul 2>&1
cls

echo ============================================
echo   Plante Uma Flor v2.0 - Servidor
echo ============================================
echo.
echo [1/2] Verificando sistema...
python test_server.py
echo.

if %ERRORLEVEL% EQU 0 (
    echo [2/2] Iniciando servidor...
    echo.
    python main.py
) else (
    echo.
    echo [ERRO] Testes falharam!
    echo Execute: python migrate_database.py
    echo.
)

pause

