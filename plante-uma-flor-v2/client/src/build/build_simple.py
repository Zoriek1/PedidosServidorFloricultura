# -*- coding: utf-8 -*-
"""
Script de build simplificado e robusto
"""
import os
import sys
import subprocess
from pathlib import Path

def install_pyinstaller():
    """Instala PyInstaller se não estiver disponível"""
    try:
        import PyInstaller
        print("✅ PyInstaller já está instalado")
        return True
    except ImportError:
        print("📦 Instalando PyInstaller...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "pyinstaller"
            ], check=True)
            print("✅ PyInstaller instalado com sucesso!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar PyInstaller: {e}")
            return False

def build_simple():
    """Build simplificado"""
    print("🚀 Plante Uma Flor v2.0 - Build Simplificado")
    print("=" * 50)
    
    # Instalar PyInstaller
    if not install_pyinstaller():
        print("❌ Não foi possível instalar PyInstaller")
        return False
    
    # Caminhos
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent
    src_dir = project_root / "src"
    dist_dir = project_root.parent / "dist"
    
    # Criar diretório de saída
    dist_dir.mkdir(exist_ok=True)
    
    print(f"📁 Diretório fonte: {src_dir}")
    print(f"📁 Diretório de saída: {dist_dir}")
    
    # Comando PyInstaller simplificado
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=PlanteUmaFlor-Client",
        "--distpath", str(dist_dir),
        "--workpath", str(dist_dir / "build"),
        "--specpath", str(dist_dir),
        str(src_dir / "main.py")
    ]
    
    print("\n📦 Executando build...")
    print(f"Comando: {' '.join(cmd)}")
    
    try:
        # Executar build
        result = subprocess.run(cmd, cwd=project_root, check=True)
        
        # Verificar se executável foi criado
        exe_path = dist_dir / "PlanteUmaFlor-Client.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / 1024 / 1024
            print(f"\n✅ SUCESSO! Executável criado:")
            print(f"📁 Local: {exe_path}")
            print(f"📊 Tamanho: {size_mb:.1f} MB")
            
            # Criar script de inicialização
            create_launcher(dist_dir)
            
            print("\n🎉 Build concluído com sucesso!")
            print("🚀 Execute o arquivo .exe para usar o aplicativo")
            return True
        else:
            print("❌ Executável não foi criado")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no build: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def create_launcher(dist_dir):
    """Cria script de inicialização"""
    launcher_path = dist_dir / "Iniciar_Cliente.bat"
    
    launcher_content = """@echo off
echo ========================================
echo   Plante Uma Flor v2.0 - Cliente
echo ========================================
echo.
echo Iniciando aplicativo...
echo.

REM Executar aplicativo
PlanteUmaFlor-Client.exe

REM Pausar se houver erro
if errorlevel 1 (
    echo.
    echo Aplicativo finalizado com erro.
    echo Verifique se o servidor está rodando.
    pause
)

echo.
echo Aplicativo finalizado.
pause
"""
    
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print(f"📝 Script de inicialização criado: {launcher_path}")

if __name__ == "__main__":
    success = build_simple()
    sys.exit(0 if success else 1)