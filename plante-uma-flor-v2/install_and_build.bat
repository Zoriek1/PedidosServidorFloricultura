@echo off
echo ========================================
echo   Plante Uma Flor v2.0 - Instalacao
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.7+ e tente novamente.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python encontrado!
echo.

REM Instalar dependências
echo Instalando dependencias...
pip install pyinstaller reportlab requests flask flask-sqlalchemy werkzeug

if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias
    pause
    exit /b 1
)

echo Dependencias instaladas com sucesso!
echo.

REM Executar build
echo Executando build do executavel...
cd client\src\build
python build_simple.py

if errorlevel 1 (
    echo ERRO: Falha no build
    pause
    exit /b 1
)

echo.
echo ========================================
echo   INSTALACAO CONCLUIDA COM SUCESSO!
echo ========================================
echo.
echo O executavel foi criado em: ..\..\..\dist\
echo Execute: Iniciar_Cliente.bat
echo.
pause