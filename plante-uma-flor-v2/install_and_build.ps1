# Plante Uma Flor v2.0 - Script de Instalação PowerShell
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Plante Uma Flor v2.0 - Instalação" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERRO: Python não encontrado!" -ForegroundColor Red
    Write-Host "Instale Python 3.7+ e tente novamente." -ForegroundColor Yellow
    Write-Host "Download: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""

# Instalar dependências
Write-Host "📦 Instalando dependências..." -ForegroundColor Yellow
$packages = @("pyinstaller", "reportlab", "requests", "flask", "flask-sqlalchemy", "werkzeug")

foreach ($package in $packages) {
    Write-Host "  Instalando $package..." -ForegroundColor Gray
    pip install $package --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Erro ao instalar $package" -ForegroundColor Red
        Read-Host "Pressione Enter para sair"
        exit 1
    }
}

Write-Host "✅ Dependências instaladas com sucesso!" -ForegroundColor Green
Write-Host ""

# Executar build
Write-Host "🔨 Executando build do executável..." -ForegroundColor Yellow
Set-Location "client\src\build"
python build_simple.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERRO: Falha no build" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   INSTALAÇÃO CONCLUÍDA COM SUCESSO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "O executável foi criado em: ..\..\..\dist\" -ForegroundColor Yellow
Write-Host "Execute: Iniciar_Cliente.bat" -ForegroundColor Yellow
Write-Host ""
Read-Host "Pressione Enter para sair"