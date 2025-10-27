# Servidor Flask - Gerenciador de Comandas

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Servidor Flask - Gerenciador de Comandas" -ForegroundColor Cyan
Write-Host "  Plante Uma Flor" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

Set-Location -Path "static"

Write-Host "Verificando dependencias..." -ForegroundColor Yellow
$flask = Get-Command pip -ErrorAction SilentlyContinue

if (-not $flask) {
    Write-Host "ERRO: pip nao encontrado. Instale Python primeiro." -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit
}

# Verificar se Flask está instalado
$flaskInstalled = pip show flask 2>$null
if (-not $flaskInstalled) {
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host "`nIniciando servidor Flask..." -ForegroundColor Green
Write-Host "URL Local: http://localhost:5000" -ForegroundColor Cyan
Write-Host "URL Rede: http://192.168.1.148:5000" -ForegroundColor Cyan
Write-Host "`nPressione Ctrl+C para parar o servidor`n" -ForegroundColor Yellow

python app.py

