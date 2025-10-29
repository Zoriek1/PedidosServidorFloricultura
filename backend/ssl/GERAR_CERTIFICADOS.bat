@echo off
:: ===================================================
:: PLANTE UMA FLOR - Gerador de Certificados SSL
:: Gera certificados HTTPS para rede local
:: ===================================================

title Gerar Certificados SSL

echo.
echo ============================================
echo    GERADOR DE CERTIFICADOS SSL
echo    Plante Uma Flor - HTTPS Local
echo ============================================
echo.

:: Verificar se mkcert está instalado
where mkcert >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] mkcert nao encontrado!
    echo.
    echo Por favor, execute primeiro: INSTALAR_MKCERT.bat
    echo.
    pause
    exit /b 1
)

echo [OK] mkcert encontrado!
echo.
mkcert -version
echo.

:: Descobrir o IP local
echo [1/4] Descobrindo IP da maquina...
echo.

for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    goto :found_ip
)

:found_ip
:: Remover espaços
set IP=%IP: =%

echo IP encontrado: %IP%
echo.

:: Confirmar IP
echo Este e o IP correto da sua maquina?
echo Se nao, pressione Ctrl+C para cancelar e edite este arquivo.
echo.
pause

:: Ir para pasta SSL
cd /d "%~dp0"

echo.
echo [2/4] Instalando CA raiz local (pode pedir senha de admin)...
echo.

:: Instalar CA raiz
mkcert -install

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha ao instalar CA raiz!
    echo Tente executar como Administrador.
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] CA raiz instalado!
echo.

echo [3/4] Gerando certificados SSL...
echo.

:: Gerar certificados
mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1 %IP% ::1

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha ao gerar certificados!
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Certificados gerados com sucesso!
echo.

echo [4/4] Verificando arquivos...
echo.

if exist "cert.pem" (
    echo [OK] cert.pem criado
) else (
    echo [ERRO] cert.pem NAO encontrado!
)

if exist "key.pem" (
    echo [OK] key.pem criado
) else (
    echo [ERRO] key.pem NAO encontrado!
)

echo.
echo ============================================
echo   CERTIFICADOS PRONTOS!
echo ============================================
echo.
echo Arquivos criados:
echo   - cert.pem (certificado publico)
echo   - key.pem (chave privada)
echo.
echo IP configurado: %IP%
echo.
echo Proximos passos:
echo   1. Execute: ..\iniciar_servidor_https.bat
echo   2. Acesse: https://%IP%:5000
echo   3. Instale o PWA normalmente!
echo.
echo Para outros dispositivos:
echo   Consulte: INSTALAR_CERTIFICADO_OUTROS_DISPOSITIVOS.md
echo.
echo ============================================
echo.
pause


