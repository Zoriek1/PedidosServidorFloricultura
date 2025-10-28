# -*- coding: utf-8 -*-
"""
Script de build otimizado para executável
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def build_executable():
    """Constrói executável otimizado"""
    
    # Caminhos
    project_root = Path(__file__).parent.parent.parent
    build_dir = project_root.parent / "dist"
    src_dir = project_root / "src"
    
    print("🚀 Iniciando build do executável...")
    
    # Limpar diretório de build
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(exist_ok=True)
    
    # Configuração do PyInstaller
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",  # Arquivo único
        "--windowed",  # Sem console
        "--name=PlanteUmaFlor-Client",
        "--icon=resources/icons/app.ico",  # Se existir
        "--add-data=resources;resources",  # Incluir recursos
        "--hidden-import=reportlab",
        "--hidden-import=requests",
        "--hidden-import=sqlite3",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.filedialog",
        "--optimize=2",  # Otimização Python
        "--strip",  # Remover símbolos de debug
        "--clean",  # Limpar cache
        f"--distpath={build_dir}",
        f"--workpath={build_dir / 'build'}",
        f"--specpath={build_dir}",
        str(src_dir / "main.py")
    ]
    
    try:
        # Executar PyInstaller
        print("📦 Executando PyInstaller...")
        result = subprocess.run(pyinstaller_cmd, cwd=project_root, check=True)
        
        # Verificar se executável foi criado
        exe_path = build_dir / "PlanteUmaFlor-Client.exe"
        if exe_path.exists():
            print(f"✅ Executável criado com sucesso: {exe_path}")
            print(f"📁 Tamanho: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
            
            # Copiar recursos necessários
            resources_dest = build_dir / "resources"
            if (src_dir / "resources").exists():
                shutil.copytree(src_dir / "resources", resources_dest)
                print("📁 Recursos copiados")
            
            # Criar script de inicialização
            create_startup_script(build_dir)
            
            print("\n🎉 Build concluído com sucesso!")
            print(f"📂 Diretório de saída: {build_dir}")
            print(f"🚀 Execute: {exe_path}")
            
        else:
            print("❌ Erro: Executável não foi criado")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no build: {e}")
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