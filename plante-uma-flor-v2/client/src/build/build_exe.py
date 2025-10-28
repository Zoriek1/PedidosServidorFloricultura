# -*- coding: utf-8 -*-
"""
Script de build otimizado para executável
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_dependencies():
    """Verifica e instala dependências necessárias"""
    print("🔍 Verificando dependências...")
    
    required_packages = ['pyinstaller', 'reportlab', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package} - não encontrado")
    
    if missing_packages:
        print(f"\n📦 Instalando dependências faltantes: {', '.join(missing_packages)}")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade"
            ] + missing_packages, check=True)
            print("✅ Dependências instaladas com sucesso!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar dependências: {e}")
            print("💡 Tente executar manualmente: pip install pyinstaller reportlab requests")
            return False
    
    return True

def build_executable():
    """Constrói executável otimizado"""
    
    # Verificar dependências primeiro
    if not check_dependencies():
        return False
    
    # Caminhos
    project_root = Path(__file__).parent.parent.parent
    build_dir = project_root.parent / "dist"
    src_dir = project_root / "src"
    
    print("\n🚀 Iniciando build do executável...")
    
    # Limpar diretório de build
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(exist_ok=True)
    
    # Configuração do PyInstaller (simplificada)
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Arquivo único
        "--windowed",  # Sem console
        "--name=PlanteUmaFlor-Client",
        "--hidden-import=reportlab",
        "--hidden-import=requests",
        "--hidden-import=sqlite3",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.filedialog",
        "--optimize=2",  # Otimização Python
        "--clean",  # Limpar cache
        f"--distpath={build_dir}",
        f"--workpath={build_dir / 'build'}",
        f"--specpath={build_dir}",
        str(src_dir / "main.py")
    ]
    
    try:
        # Executar PyInstaller
        print("📦 Executando PyInstaller...")
        result = subprocess.run(pyinstaller_cmd, cwd=project_root, check=True, 
                              capture_output=True, text=True)
        
        # Verificar se executável foi criado
        exe_path = build_dir / "PlanteUmaFlor-Client.exe"
        if exe_path.exists():
            print(f"✅ Executável criado com sucesso: {exe_path}")
            print(f"📁 Tamanho: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
            
            # Copiar recursos necessários
            resources_src = src_dir / "resources"
            resources_dest = build_dir / "resources"
            if resources_src.exists():
                shutil.copytree(resources_src, resources_dest)
                print("📁 Recursos copiados")
            
            # Criar script de inicialização
            create_startup_script(build_dir)
            
            print("\n🎉 Build concluído com sucesso!")
            print(f"📂 Diretório de saída: {build_dir}")
            print(f"🚀 Execute: {exe_path}")
            
        else:
            print("❌ Erro: Executável não foi criado")
            print("📋 Saída do PyInstaller:")
            print(result.stdout)
            if result.stderr:
                print("❌ Erros:")
                print(result.stderr)
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no build: {e}")
        print("📋 Saída do PyInstaller:")
        if hasattr(e, 'stdout') and e.stdout:
            print(e.stdout)
        if hasattr(e, 'stderr') and e.stderr:
            print("❌ Erros:")
            print(e.stderr)
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    
    return True

def create_startup_script(build_dir: Path):
    """Cria script de inicialização"""
    startup_script = build_dir / "start_client.bat"
    
    script_content = """@echo off
echo Iniciando Plante Uma Flor v2.0...
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado!
    echo Instale Python 3.7+ e tente novamente.
    pause
    exit /b 1
)

REM Executar aplicação
PlanteUmaFlor-Client.exe

REM Pausar se houver erro
if errorlevel 1 (
    echo.
    echo Aplicação finalizada com erro.
    pause
)
"""
    
    with open(startup_script, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("📝 Script de inicialização criado")

def build_with_nuitka():
    """Build alternativo com Nuitka (mais otimizado)"""
    print("🚀 Tentando build com Nuitka...")
    
    project_root = Path(__file__).parent.parent.parent
    src_dir = project_root / "src"
    
    nuitka_cmd = [
        "nuitka",
        "--standalone",
        "--windows-disable-console",
        "--output-dir=dist",
        "--output-filename=PlanteUmaFlor-Client.exe",
        "--include-data-dir=resources=resources",
        "--enable-plugin=tk-inter",
        "--assume-yes-for-downloads",
        str(src_dir / "main.py")
    ]
    
    try:
        subprocess.run(nuitka_cmd, cwd=project_root, check=True)
        print("✅ Build com Nuitka concluído!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ Nuitka não disponível, usando PyInstaller")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🌺 Plante Uma Flor v2.0 - Build Script")
    print("=" * 50)
    
    # Tentar Nuitka primeiro (mais otimizado)
    if not build_with_nuitka():
        # Fallback para PyInstaller
        build_executable()
    
    print("\n✨ Build finalizado!")