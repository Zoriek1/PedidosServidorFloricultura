@echo off
echo ================================================
echo   Servidor Flask - Gerenciador de Comandas
echo   Plante Uma Flor
echo ================================================
echo.

cd static

echo Verificando dependencias...
pip show flask flask-sqlalchemy >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    echo.
)

echo.
echo Iniciando servidor Flask...
echo URL: http://localhost:5000
echo URL Rede: http://192.168.1.148:5000
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

python app.py

pause

