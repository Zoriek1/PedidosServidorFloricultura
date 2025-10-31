@echo off
:: ===================================================
:: PLANTE UMA FLOR - Testar Servidor Corrigido
:: Testa se o servidor inicia sem erros de encoding
:: ===================================================

title Testar Servidor Corrigido

cd /d "%~dp0"

echo.
echo ============================================
echo   TESTE DO SERVIDOR HTTPS CORRIGIDO
echo ============================================
echo.
echo Emojis removidos dos prints Python
echo Encoding UTF-8 configurado
echo.
echo Este teste vai iniciar o servidor por 10 segundos
echo e depois parar automaticamente.
echo.
pause

echo.
echo [1/3] Iniciando servidor HTTPS...
echo.

:: Iniciar servidor em background
start /B python main.py --https

:: Aguardar 5 segundos
echo Aguardando 5 segundos para o servidor iniciar...
timeout /t 5 /nobreak >nul

echo.
echo [2/3] Verificando se esta rodando...
echo.

:: Verificar porta
netstat -ano | findstr :5000 >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Servidor INICIOU com sucesso na porta 5000!
    echo.
    echo Teste acessando:
    echo   https://192.168.1.148:5000
    echo   https://localhost:5000
    echo.
) else (
    echo [ERRO] Servidor NAO esta rodando!
    echo Verifique o log acima para erros.
    echo.
    pause
    exit /b 1
)

echo [3/3] Aguardando 10 segundos antes de parar...
timeout /t 10 /nobreak

echo.
echo Parando servidor...

:: Parar servidor
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo.
echo ============================================
echo   TESTE CONCLUIDO!
echo ============================================
echo.
echo Se o servidor iniciou e voce conseguiu acessar,
echo tudo esta funcionando corretamente!
echo.
echo Agora pode usar:
echo   - iniciar_servidor_https_invisivel.vbs (invisivel)
echo   - python main.py --https (com janela)
echo.
pause

