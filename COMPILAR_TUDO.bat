@echo off
echo ================================================
echo   Compilando TODOS os Executaveis
echo   Plante Uma Flor
echo ================================================
echo.

echo Verificando PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller nao encontrado!
    echo Instalando...
    pip install pyinstaller
    echo.
)

echo.
echo [1/3] Compilando PDFgen.exe...
echo.
cd Clientes
pyinstaller PDFgen.spec
cd ..

echo.
echo [2/3] Compilando Gerador_De_Pedidos.exe...
echo.
cd Servidor
pyinstaller --onefile --console --name=Gerador_De_Pedidos Gerador_De_Pedidos.py
cd ..

echo.
echo [3/3] Compilando Iniciar_Servidor.exe...
echo.
cd Servidor
pyinstaller --onefile --console --name=Iniciar_Servidor Iniciar_Servidor.py
cd ..

echo.
echo ================================================
echo   Compilacao Concluida!
echo ================================================
echo.
echo Arquivos criados:
echo   - Clientes\dist\PDFgen.exe
echo   - Servidor\dist\Gerador_De_Pedidos.exe
echo   - Servidor\dist\Iniciar_Servidor.exe
echo.

pause

