@echo off
:: ====================================================
:: PARAR SERVIDOR COM PERMISSOES DE ADMINISTRADOR
:: ====================================================

:: Verificar se já está rodando como admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ============================================
    echo   PRECISA DE PERMISSAO DE ADMINISTRADOR
    echo ============================================
    echo.
    echo Solicitando permissoes...
    echo.
    
    :: Executar novamente como admin
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

title Parar Servidor (Admin)

echo.
echo ============================================
echo   PARAR SERVIDORES (COM ADMIN)
echo ============================================
echo.

echo Matando TODOS os processos na porta 5000...
echo.

:: Listar e matar todos os PIDs na porta 5000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    echo Matando PID: %%a
    taskkill /F /PID %%a 2>nul
    if errorlevel 1 (
        echo   [ERRO] Nao foi possivel matar PID %%a
    ) else (
        echo   [OK] PID %%a finalizado
    )
)

echo.
echo Matando todos os processos Python...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
taskkill /F /IM py.exe 2>nul

echo.
echo Aguardando 2 segundos...
timeout /t 2 /nobreak >nul

echo.
echo ============================================
echo   VERIFICANDO RESULTADO...
echo ============================================
echo.

netstat -ano | findstr :5000 | findstr LISTENING

if %errorlevel% equ 0 (
    echo.
    echo [AVISO] AINDA HA PROCESSOS!
    echo.
    echo Use o Gerenciador de Tarefas:
    echo 1. Ctrl+Shift+Esc
    echo 2. Aba "Detalhes"
    echo 3. Finalize todos os "python.exe"
    echo.
) else (
    echo.
    echo ============================================
    echo   SUCESSO! Porta 5000 esta LIVRE!
    echo ============================================
    echo.
    echo Agora voce pode:
    echo   1. Gerar certificados: cd ssl ^& GERAR_CERTIFICADOS_AUTO.bat
    echo   2. Iniciar HTTPS: cd .. ^& python main.py --https
    echo.
)

echo.
pause

