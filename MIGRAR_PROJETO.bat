@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
cls

echo ============================================
echo   Plante Uma Flor v2.0
echo   MIGRAÇÃO DE PROJETO
echo ============================================
echo.
echo Este script vai mover o projeto de:
echo.
echo   DE: %~dp0
echo   PARA: C:\Gestor de Pedidos Plante uma flor\
echo.
echo ============================================
echo.
echo IMPORTANTE:
echo - Certifique-se que executou PREPARAR_MIGRACAO.bat
echo - Feche todos os editores de código (VS Code, etc)
echo - Feche o Windows Explorer nesta pasta
echo.
echo ============================================
pause
cls

echo ============================================
echo   INICIANDO MIGRAÇÃO
echo ============================================
echo.

REM Salvar diretório atual (remover barra final)
set SOURCE_DIR=%~dp0
set SOURCE_DIR=%SOURCE_DIR:~0,-1%
set "DEST_DIR=C:\Gestor de Pedidos Plante uma flor"

echo [1/6] Parando processos Python...
echo.

REM Parar servidor na porta 5000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000" ^| findstr "LISTENING"') do (
    set PID=%%a
    taskkill /F /PID %%a >NUL 2>&1
    echo     ✓ Processo na porta 5000 parado (PID: %%a)
)

REM Parar todos os processos Python
taskkill /F /IM python.exe >NUL 2>&1
taskkill /F /IM pythonw.exe >NUL 2>&1
echo     ✓ Todos os processos Python parados

REM Aguardar liberação
timeout /t 3 /nobreak >nul
echo     ✓ Arquivos liberados

cls
echo ============================================
echo   MIGRAÇÃO EM ANDAMENTO
echo ============================================
echo.

echo [2/6] Limpando arquivos temporários...
echo.

REM Limpar __pycache__ recursivamente
echo     • Removendo pastas __pycache__...
for /d /r "%SOURCE_DIR%" %%d in (__pycache__) do (
    if exist "%%d" (
        rd /s /q "%%d" 2>nul
        if exist "%%d" (
            echo     ⚠ Falha ao remover: %%d
        )
    )
)
echo     ✓ Pastas __pycache__ removidas

REM Limpar arquivos .pyc isolados
echo     • Removendo arquivos .pyc...
del /s /q "%SOURCE_DIR%*.pyc" >nul 2>&1
echo     ✓ Arquivos .pyc removidos

REM Opcional: Limpar logs antigos (comentado por segurança)
REM echo     • Limpando logs antigos...
REM del /q "%SOURCE_DIR%Servidor\logs\*.log" >nul 2>&1
REM echo     ✓ Logs limpos

echo.
echo [3/6] Verificando diretório destino...
echo.

if not exist "%DEST_DIR%" (
    echo     • Criando diretório destino...
    mkdir "%DEST_DIR%" 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo     ❌ ERRO: Não foi possível criar o diretório!
        echo     ❌ Verifique permissões e se C:\ está acessível
        echo.
        pause
        exit /b 1
    )
    echo     ✓ Diretório criado
) else (
    echo     ℹ Diretório destino já existe
    echo.
    echo     ATENÇÃO: O diretório de destino já existe!
    echo     %DEST_DIR%
    echo.
    choice /C SN /M "Deseja continuar e sobrescrever arquivos existentes?"
    if errorlevel 2 (
        echo.
        echo     ⚠ Migração cancelada pelo usuário
        pause
        exit /b 0
    )
)

echo.
echo [4/6] Copiando arquivos para o novo local...
echo.
echo     Este processo pode levar alguns minutos...
echo     Aguarde...
echo.

REM Usar robocopy (mais robusto que move/xcopy)
REM /E = Copiar subdiretórios incluindo vazios
REM /COPYALL = Copiar todas as informações de arquivo
REM /R:3 = 3 tentativas em caso de falha
REM /W:5 = Aguardar 5 segundos entre tentativas
REM /NFL = Não listar arquivos (menos verboso)
REM /NDL = Não listar diretórios (menos verboso)
REM /NP = Não mostrar progresso por arquivo
REM /XD = Excluir diretórios

robocopy "%SOURCE_DIR%" "%DEST_DIR%" /E /COPYALL /R:3 /W:5 /NFL /NDL /NP /XD .git node_modules __pycache__

REM Robocopy retorna códigos diferentes:
REM 0-7 = Sucesso, 8+ = Erro
if %ERRORLEVEL% GEQ 8 (
    echo.
    echo     ❌ ERRO na cópia de arquivos!
    echo     ❌ Código de erro: %ERRORLEVEL%
    echo.
    echo     Os arquivos originais NÃO foram removidos.
    echo     Você pode tentar novamente ou copiar manualmente.
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo     ✓ Arquivos copiados com sucesso!
)

echo.
echo [5/6] Verificando integridade...
echo.

REM Verificar se arquivos críticos existem no destino
set VERIFICATION_FAILED=0

if not exist "%DEST_DIR%\Servidor\run\main.py" (
    echo     ❌ ERRO: main.py não encontrado no destino!
    set VERIFICATION_FAILED=1
)

if not exist "%DEST_DIR%\Servidor\static\database.db" (
    echo     ⚠ AVISO: database.db não encontrado no destino!
    echo     ⚠ O banco de dados pode não ter sido copiado
)

if not exist "%DEST_DIR%\Clientes\PDFgen.py" (
    echo     ❌ ERRO: PDFgen.py não encontrado no destino!
    set VERIFICATION_FAILED=1
)

if %VERIFICATION_FAILED% EQU 1 (
    echo.
    echo     ❌ VERIFICAÇÃO FALHOU!
    echo.
    echo     Os arquivos originais NÃO foram removidos.
    echo     Verifique manualmente o que aconteceu.
    echo.
    pause
    exit /b 1
)

echo     ✓ Arquivos críticos verificados no destino

echo.
echo [6/6] Confirmação para remover pasta antiga...
echo.

echo     ============================================
echo     CONFIRMAÇÃO FINAL
echo     ============================================
echo.
echo     Os arquivos foram copiados com sucesso para:
echo     %DEST_DIR%
echo.
echo     Deseja REMOVER a pasta antiga?
echo     %SOURCE_DIR%
echo.
echo     ATENÇÃO: Esta ação NÃO pode ser desfeita!
echo.
echo     Recomendação: Teste o projeto no novo local
echo     antes de remover a pasta antiga.
echo.

choice /C SN /M "Remover pasta antiga agora?"

if errorlevel 2 (
    echo.
    echo     ℹ Pasta antiga MANTIDA
    echo.
    echo     Você pode removê-la manualmente depois de
    echo     verificar que tudo funciona no novo local.
    echo.
    goto :fim
)

echo.
echo     • Removendo pasta antiga...
echo     • Aguarde...
echo.

REM Tentar remover a pasta antiga
cd /d C:\
rd /s /q "%SOURCE_DIR%" 2>nul

if exist "%SOURCE_DIR%" (
    echo     ⚠ AVISO: Não foi possível remover completamente
    echo     ⚠ Alguns arquivos podem ainda estar em uso
    echo.
    echo     Você pode:
    echo     1. Reiniciar o computador e remover manualmente
    echo     2. Usar a Lixeira para remover com segurança
    echo.
) else (
    echo     ✓ Pasta antiga removida com sucesso!
)

:fim
echo.
echo ============================================
echo   ✓ MIGRAÇÃO CONCLUÍDA!
echo ============================================
echo.
echo Próximos passos:
echo.
echo 1. Navegue até: %DEST_DIR%
echo.
echo 2. Execute VALIDAR_MIGRACAO.bat para testar
echo.
echo 3. Inicie o servidor normalmente:
echo    %DEST_DIR%\Servidor\run\INICIAR_AQUI.bat
echo.
echo ============================================
echo.

REM Oferecer para abrir o novo local
choice /C SN /M "Deseja abrir o novo local no Windows Explorer?"
if errorlevel 1 if not errorlevel 2 (
    explorer "%DEST_DIR%"
)

echo.
pause

