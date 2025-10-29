@echo off
:: ===================================================
:: PLANTE UMA FLOR - Gerador de Certificados (Auto)
:: Detecta automaticamente mkcert (local ou sistema)
:: ===================================================

title Gerar Certificados SSL

echo.
echo ============================================
echo    GERADOR DE CERTIFICADOS SSL
echo    Plante Uma Flor - HTTPS Local
echo ============================================
echo.

cd /d "%~dp0"

:: Verificar se mkcert está no PATH (sistema)
where mkcert >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] mkcert encontrado no sistema!
    set MKCERT_CMD=mkcert
    goto :mkcert_found
)

:: Verificar se mkcert existe na pasta local
if exist "mkcert.exe" (
    echo [OK] mkcert.exe encontrado na pasta local!
    set MKCERT_CMD=.\mkcert.exe
    goto :mkcert_found
)

:: Se não encontrou em nenhum lugar
echo [ERRO] mkcert nao encontrado!
echo.
echo O mkcert deve estar:
echo   1. No PATH do sistema (execute: where mkcert)
echo   2. Ou nesta pasta como mkcert.exe
echo.
echo Execute: INSTALAR_MKCERT_SIMPLES.bat
echo.
pause
exit /b 1

:mkcert_found
echo.
%MKCERT_CMD% -version
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

echo Este e o IP correto da sua maquina?
echo Se nao, pressione Ctrl+C e edite este arquivo.
echo.
pause

echo.
echo [2/4] Instalando CA raiz local...
echo (Pode pedir senha de administrador - isso e normal!)
echo.

:: Instalar CA raiz
%MKCERT_CMD% -install

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha ao instalar CA raiz!
    echo.
    echo Isso requer permissoes de administrador.
    echo Tente:
    echo 1. Clique com botao direito neste arquivo
    echo 2. "Executar como administrador"
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
%MKCERT_CMD% -cert-file cert.pem -key-file key.pem localhost 127.0.0.1 %IP% ::1

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha ao gerar certificados!
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Certificados gerados!
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
echo   1. Volte para: ..\
echo   2. Execute: abrir_sistema_https.bat
echo   3. Acesse: https://%IP%:5000
echo.
echo Para instalar em outros dispositivos:
echo   1. Execute: mkcert -CAROOT
echo   2. Copie o arquivo rootCA.pem
echo   3. Leia: INSTALAR_CERTIFICADO_OUTROS_DISPOSITIVOS.md
echo.
echo ============================================
echo.
pause

