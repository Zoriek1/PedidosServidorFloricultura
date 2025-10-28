@echo off
chcp 65001 >nul 2>&1
cls

echo ============================================
echo   PDFgen.exe - Compilação Automática
echo   Plante Uma Flor v2.0
echo ============================================
echo.

REM Verificar se está na pasta Clientes
if not exist "PDFgen.py" (
    echo [ERRO] Execute este script na pasta Clientes!
    echo.
    pause
    exit /b 1
)

REM Verificar se PyInstaller está instalado
echo [1/4] Verificando PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo.
    echo PyInstaller não encontrado. Instalando...
    pip install pyinstaller
    echo.
)

REM Verificar dependências
echo.
echo [2/4] Verificando dependências...
pip install -r requirements.txt --quiet
echo Dependências OK!

REM Limpar builds antigos
echo.
echo [3/4] Limpando builds antigos...
if exist "build\" rmdir /s /q "build"
if exist "dist\" rmdir /s /q "dist"
if exist "PDFgen.exe" del /q "PDFgen.exe"
echo Limpeza concluída!

REM Compilar
echo.
echo [4/4] Compilando PDFgen.exe...
echo (Isso pode levar alguns minutos...)
echo.
pyinstaller PDFgen.spec --clean --noconfirm

REM Verificar se compilou
if exist "dist\PDFgen.exe" (
    echo.
    echo ============================================
    echo   COMPILAÇÃO CONCLUÍDA COM SUCESSO! ✓
    echo ============================================
    echo.
    echo Executável criado em: dist\PDFgen.exe
    echo.
    echo Funcionalidades incluídas:
    echo   ✓ Descoberta automática de servidor
    echo   ✓ Geração de PDF
    echo   ✓ Banco de dados SQLite
    echo   ✓ Integração com painel v2.0
    echo.
    
    REM Copiar para raiz (opcional)
    copy "dist\PDFgen.exe" "PDFgen.exe" >nul 2>&1
    if exist "PDFgen.exe" (
        echo   ✓ Cópia criada: PDFgen.exe (raiz)
        echo.
    )
    
    echo Pronto para distribuir!
    echo.
) else (
    echo.
    echo ============================================
    echo   ERRO NA COMPILAÇÃO!
    echo ============================================
    echo.
    echo Verifique os erros acima.
    echo.
)

pause

