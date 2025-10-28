@echo off
echo ========================================
echo   Plante Uma Flor v2.0 - Cliente
echo ========================================
echo.
echo Iniciando aplicativo...
echo.

REM Executar aplicativo
PlanteUmaFlor-Client.exe

REM Pausar se houver erro
if errorlevel 1 (
    echo.
    echo Aplicativo finalizado com erro.
    echo Verifique se o servidor está rodando.
    pause
)

echo.
echo Aplicativo finalizado.
pause
