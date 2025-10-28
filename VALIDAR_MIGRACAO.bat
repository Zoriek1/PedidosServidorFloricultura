@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
cls

echo ============================================
echo   Plante Uma Flor v2.0
echo   VALIDAÇÃO PÓS-MIGRAÇÃO
echo ============================================
echo.
echo Este script valida se o projeto foi migrado
echo corretamente e está pronto para uso.
echo.
echo ============================================
pause
echo.

echo [VALIDAÇÃO] Verificando estrutura do projeto...
echo.

REM Obter diretório atual
set PROJECT_DIR=%~dp0

echo Diretório do projeto: %PROJECT_DIR%
echo.

set ERRORS=0

echo [1/8] Verificando arquivos do Servidor...
if exist "%PROJECT_DIR%Servidor\run\main.py" (
    echo     ✓ main.py encontrado
) else (
    echo     ❌ main.py NÃO encontrado
    set /a ERRORS+=1
)

if exist "%PROJECT_DIR%Servidor\run\config.json" (
    echo     ✓ config.json encontrado
) else (
    echo     ⚠ config.json NÃO encontrado (será criado no primeiro uso)
)

if exist "%PROJECT_DIR%Servidor\run\app\__init__.py" (
    echo     ✓ app/__init__.py encontrado
) else (
    echo     ❌ app/__init__.py NÃO encontrado
    set /a ERRORS+=1
)

echo.
echo [2/8] Verificando banco de dados...
if exist "%PROJECT_DIR%Servidor\static\database.db" (
    echo     ✓ database.db encontrado
    
    REM Verificar tamanho do arquivo (opcional)
    echo     ✓ Arquivo verificado
) else (
    echo     ⚠ database.db NÃO encontrado (será criado no primeiro uso)
)

echo.
echo [3/8] Verificando cliente PDFgen...
if exist "%PROJECT_DIR%Clientes\PDFgen.py" (
    echo     ✓ PDFgen.py encontrado
) else (
    echo     ❌ PDFgen.py NÃO encontrado
    set /a ERRORS+=1
)

if exist "%PROJECT_DIR%Clientes\PDFgen.exe" (
    echo     ✓ PDFgen.exe encontrado
) else (
    echo     ⚠ PDFgen.exe NÃO encontrado
)

echo.
echo [4/8] Verificando arquivos de fonte...
if exist "%PROJECT_DIR%Clientes\Montserrat-VariableFont_wght.ttf" (
    echo     ✓ Fontes Montserrat encontradas
) else (
    echo     ⚠ Fontes Montserrat NÃO encontradas
)

echo.
echo [5/8] Verificando scripts de inicialização...
if exist "%PROJECT_DIR%Servidor\run\INICIAR_AQUI.bat" (
    echo     ✓ INICIAR_AQUI.bat encontrado
) else (
    echo     ❌ INICIAR_AQUI.bat NÃO encontrado
    set /a ERRORS+=1
)

if exist "%PROJECT_DIR%Servidor\run\INICIAR_SERVIDOR_BACKGROUND.vbs" (
    echo     ✓ INICIAR_SERVIDOR_BACKGROUND.vbs encontrado
) else (
    echo     ❌ INICIAR_SERVIDOR_BACKGROUND.vbs NÃO encontrado
    set /a ERRORS+=1
)

if exist "%PROJECT_DIR%Servidor\run\PARAR_SERVIDOR.bat" (
    echo     ✓ PARAR_SERVIDOR.bat encontrado
) else (
    echo     ❌ PARAR_SERVIDOR.bat NÃO encontrado
    set /a ERRORS+=1
)

echo.
echo [6/8] Verificando dependências Python (Servidor)...
if exist "%PROJECT_DIR%Servidor\run\requirements.txt" (
    echo     ✓ requirements.txt encontrado
) else (
    echo     ⚠ requirements.txt NÃO encontrado
)

echo.
echo [7/8] Verificando dependências Python (Cliente)...
if exist "%PROJECT_DIR%Clientes\requirements.txt" (
    echo     ✓ requirements.txt encontrado
) else (
    echo     ⚠ requirements.txt NÃO encontrado
)

echo.
echo [8/8] Testando instalação Python...
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo     ✓ Python está instalado e acessível
    python --version
) else (
    echo     ❌ Python NÃO está acessível no PATH
    echo     ❌ Instale Python 3.8+ e adicione ao PATH
    set /a ERRORS+=1
)

echo.
echo ============================================
echo   RESULTADO DA VALIDAÇÃO
echo ============================================
echo.

if %ERRORS% EQU 0 (
    echo ✓✓✓ VALIDAÇÃO BEM-SUCEDIDA! ✓✓✓
    echo.
    echo Todos os arquivos críticos estão presentes.
    echo O projeto está pronto para uso!
    echo.
    echo ============================================
    echo   PRÓXIMOS PASSOS
    echo ============================================
    echo.
    echo 1. Instalar dependências do Servidor:
    echo    cd "%PROJECT_DIR%Servidor\run"
    echo    pip install -r requirements.txt
    echo.
    echo 2. Instalar dependências do Cliente:
    echo    cd "%PROJECT_DIR%Clientes"
    echo    pip install -r requirements.txt
    echo.
    echo 3. Iniciar o servidor:
    echo    "%PROJECT_DIR%Servidor\run\INICIAR_AQUI.bat"
    echo.
    echo 4. Executar o cliente:
    echo    "%PROJECT_DIR%Clientes\PDFgen.exe"
    echo    ou
    echo    python "%PROJECT_DIR%Clientes\PDFgen.py"
    echo.
) else (
    echo ❌❌❌ VALIDAÇÃO FALHOU! ❌❌❌
    echo.
    echo Foram encontrados %ERRORS% erro(s) crítico(s).
    echo.
    echo Possíveis causas:
    echo - A migração não foi concluída corretamente
    echo - Arquivos foram corrompidos durante a cópia
    echo - Você está executando do diretório errado
    echo.
    echo Recomendação:
    echo - Execute MIGRAR_PROJETO.bat novamente
    echo - OU copie manualmente a pasta completa
    echo.
)

echo ============================================
echo.

REM Oferecer teste rápido do servidor
if %ERRORS% EQU 0 (
    echo.
    choice /C SN /M "Deseja tentar iniciar o servidor agora para teste?"
    if errorlevel 1 if not errorlevel 2 (
        echo.
        echo Iniciando servidor em modo teste...
        echo Pressione Ctrl+C para parar
        echo.
        timeout /t 3 /nobreak >nul
        cd /d "%PROJECT_DIR%Servidor\run"
        python main.py
    )
)

echo.
pause

