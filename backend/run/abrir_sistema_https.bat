@echo off
:: ===================================================
:: PLANTE UMA FLOR - Abrir Sistema HTTPS
:: Inicia o servidor HTTPS e abre no navegador
:: ===================================================

title Plante Uma Flor - Inicializando...

cd /d "%~dp0"

echo.
echo ============================================
echo    PLANTE UMA FLOR - Sistema HTTPS
echo ============================================
echo.

:: Verificar certificados
if not exist "ssl\cert.pem" (
    echo [ERRO] Certificados nao encontrados!
    echo.
    echo Execute primeiro:
    echo   1. ssl\INSTALAR_MKCERT.bat
    echo   2. ssl\GERAR_CERTIFICADOS.bat
    echo.
    pause
    exit /b 1
)

:: Iniciar servidor invisível
echo [1/2] Iniciando servidor HTTPS em background...
start /min "" wscript.exe "iniciar_servidor_https_invisivel.vbs"

:: Aguardar servidor iniciar
echo [2/2] Aguardando servidor inicializar...
timeout /t 5 /nobreak >nul

:: Descobrir IP local
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    goto :found_ip
)

:found_ip
set IP=%IP: =%

echo.
echo [OK] Servidor HTTPS iniciado!
echo.
echo Abrindo navegador...

:: Abrir no navegador padrão
start https://localhost:5000

echo.
echo ============================================
echo   SERVIDOR RODANDO EM BACKGROUND
echo ============================================
echo.
echo Acesse de outros dispositivos:
echo   https://%IP%:5000
echo.
echo Para parar o servidor:
echo   Execute: parar_servidor.bat
echo.
echo ============================================
echo.

timeout /t 3
exit


