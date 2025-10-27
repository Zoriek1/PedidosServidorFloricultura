# Script de Automação do Servidor Flask
# Plante Uma Flor - Gerenciador de Comandas

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Automação do Servidor Flask" -ForegroundColor Cyan
Write-Host "  Plante Uma Flor" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

# Verificar se Python está instalado
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "ERRO: Python não encontrado!" -ForegroundColor Red
    Write-Host "Instale Python 3.7 ou superior." -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "Versão do Python:" -ForegroundColor Green
python --version

# Navegar para o diretório do script
Set-Location -Path $PSScriptRoot

# Verificar dependências
Write-Host "`nVerificando dependências..." -ForegroundColor Yellow
$flaskInstalled = pip show flask 2>$null
if (-not $flaskInstalled) {
    Write-Host "Instalando dependências..." -ForegroundColor Yellow
    pip install -r static\requirements.txt
}

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "Configuração da Automação" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Início automático: 08:00" -ForegroundColor Green
Write-Host "Encerramento automático: 18:30" -ForegroundColor Green
Write-Host "Monitoramento: A cada 60 segundos" -ForegroundColor Green
Write-Host "================================================`n" -ForegroundColor Cyan

Write-Host "IMPORTANTE:" -ForegroundColor Yellow
Write-Host "  - Mantenha esta janela aberta" -ForegroundColor White
Write-Host "  - Para parar o servidor, pressione Ctrl+C" -ForegroundColor White
Write-Host "  - O servidor será reiniciado automaticamente se cair" -ForegroundColor White
Write-Host "  - O servidor inicia às 08:00 ou imediatamente se já passou desse horário" -ForegroundColor White
Write-Host "  - O servidor encerra automaticamente às 18:30`n" -ForegroundColor White

Write-Host "Iniciando automação...`n" -ForegroundColor Green

# Iniciar o script Python
python iniciar_automático.py

# Se chegou aqui, o script foi encerrado
Write-Host "`nScript encerrado." -ForegroundColor Yellow
Read-Host "Pressione Enter para sair"

