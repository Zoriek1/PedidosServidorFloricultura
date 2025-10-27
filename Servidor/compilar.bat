@echo off
echo ================================================
echo   Compilando Executaveis
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
echo Compilando Gerador_De_Pedidos.exe...
pyinstaller --onefile --console --name=Gerador_De_Pedidos --icon=Buques.ico Gerador_De_Pedidos.py

echo.
echo Compilando Iniciar_Servidor.exe...
pyinstaller --onefile --console --name=Iniciar_Servidor --icon=Buques.ico Iniciar_Servidor.py

echo.
echo ================================================
echo   Compilacao Concluida!
echo ================================================
echo.
echo Arquivos criados em: dist\
echo.
echo Executaveis:
echo   - dist\Gerador_De_Pedidos.exe
echo   - dist\Iniciar_Servidor.exe
echo.

pause

