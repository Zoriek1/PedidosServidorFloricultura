@echo off
REM Script de Automação do Servidor Flask
REM Plante Uma Flor - Gerenciador de Comandas

echo ================================================
echo   Automação do Servidor Flask
echo   Plante Uma Flor
echo ================================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.7 ou superior.
    pause
    exit /b 1
)

REM Navegar para o diretório do script
cd /d "%~dp0"

REM Verificar dependências
echo Verificando dependencias...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r static\requirements.txt
)

echo.
echo Iniciando automacao do servidor Flask...
echo.
echo Configuracao:
echo   - Inicio: 08:00
echo   - Encerramento: 18:30
echo   - Monitoramento: A cada 60 segundos
echo.
echo IMPORTANTE:
echo   - Mantenha esta janela aberta
echo   - Para parar o servidor, pressione Ctrl+C
echo   - O servidor sera reiniciado automaticamente se cair
echo.
echo Pressione qualquer tecla para continuar...
pause >nul

REM Iniciar o script Python
python iniciar_automático.py

pause

