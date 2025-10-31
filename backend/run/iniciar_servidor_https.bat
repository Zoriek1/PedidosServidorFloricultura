@echo off
:: ===================================================
:: PLANTE UMA FLOR - Iniciar Servidor HTTPS
:: Inicia o servidor Flask com SSL/HTTPS
:: ===================================================

title Plante Uma Flor - Servidor HTTPS

echo.
echo ============================================
echo    PLANTE UMA FLOR - SERVIDOR HTTPS
echo ============================================
echo.

:: Mudar para o diretório do backend (pasta pai)
cd /d "%~dp0\.."

:: Verificar se os certificados existem
if not exist "ssl\cert.pem" (
    echo [ERRO] Certificados SSL nao encontrados!
    echo.
    echo Primeiro, gere os certificados:
    echo   1. Abra: ssl\INSTALAR_MKCERT.bat
    echo   2. Depois: ssl\GERAR_CERTIFICADOS.bat
    echo   3. Execute este arquivo novamente
    echo.
    pause
    exit /b 1
)

echo [OK] Certificados SSL encontrados!
echo.

:: Ativar ambiente virtual Python se existir
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Ativando ambiente virtual...
    call venv\Scripts\activate.bat
)

:: Verificar se Python está disponível
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado no PATH!
    echo.
    echo Certifique-se de que o Python esta instalado.
    echo.
    pause
    exit /b 1
)

echo [INFO] Iniciando servidor em modo HTTPS...
echo.
echo ============================================
echo   O servidor vai abrir na porta 5000
echo   Acesse: https://localhost:5000
echo   ou: https://Gestor-pedidos.local:5000
echo.
echo   Para parar: Pressione Ctrl+C
echo ============================================
echo.
echo [INFO] Modo estavel (sem auto-reload)
echo.

:: Iniciar servidor em modo HTTPS com --no-reload (mais estável)
python main.py --https --no-reload

:: Se o servidor parou
echo.
echo [INFO] Servidor encerrado.
pause


