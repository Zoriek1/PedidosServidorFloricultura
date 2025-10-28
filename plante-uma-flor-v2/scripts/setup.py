# -*- coding: utf-8 -*-
"""
Script de configuração inicial do sistema
"""
import sys
import os
import subprocess
from pathlib import Path

def install_dependencies():
    """Instala dependências necessárias"""
    print("📦 Instalando dependências...")
    
    # Cliente
    client_requirements = Path(__file__).parent.parent / "client" / "src" / "build" / "requirements.txt"
    if client_requirements.exists():
        print("  🔧 Instalando dependências do cliente...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(client_requirements)
            ], check=True)
            print("  ✅ Dependências do cliente instaladas")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Erro ao instalar dependências do cliente: {e}")
            return False
    
    # Servidor
    server_requirements = Path(__file__).parent.parent / "server" / "src" / "requirements.txt"
    if server_requirements.exists():
        print("  🔧 Instalando dependências do servidor...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(server_requirements)
            ], check=True)
            print("  ✅ Dependências do servidor instaladas")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Erro ao instalar dependências do servidor: {e}")
            return False
    
    return True

def create_directories():
    """Cria diretórios necessários"""
    print("📁 Criando diretórios...")
    
    base_dir = Path(__file__).parent.parent
    
    directories = [
        base_dir / "client" / "logs",
        base_dir / "client" / "dist",
        base_dir / "server" / "logs",
        base_dir / "server" / "database",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directory}")
    
    return True

def copy_fonts():
    """Copia fontes para o cliente"""
    print("🔤 Configurando fontes...")
    
    # Copiar fontes do projeto original se existirem
    original_fonts = Path(__file__).parent.parent.parent / "Clientes" / "fonts"
    client_fonts = Path(__file__).parent.parent / "client" / "src" / "resources" / "fonts"
    
    if original_fonts.exists() and client_fonts.exists():
        import shutil
        for font_file in original_fonts.glob("*.ttf"):
            shutil.copy2(font_file, client_fonts)
            print(f"  ✅ {font_file.name}")
    
    return True

def create_config_files():
    """Cria arquivos de configuração"""
    print("⚙️ Criando arquivos de configuração...")
    
    # Configuração do cliente
    client_config = Path(__file__).parent.parent / "client" / "src" / "resources" / "config.json"
    if not client_config.exists():
        config_content = '''{
  "app": {
    "name": "Plante Uma Flor v2.0",
    "version": "2.0.0"
  },
  "server": {
    "base_url": "http://192.168.1.148:5000",
    "timeout": 5
  },
  "database": {
    "path": "Documents/Pedidos-Floricultura/pedidos.db"
  }
}'''
        client_config.write_text(config_content, encoding='utf-8')
        print("  ✅ Configuração do cliente criada")
    
    return True

def test_installation():
    """Testa se a instalação foi bem-sucedida"""
    print("🧪 Testando instalação...")
    
    try:
        # Testar importações
        import flask
        import flask_sqlalchemy
        import reportlab
        import requests
        print("  ✅ Dependências Python importadas com sucesso")
        
        # Testar estrutura de diretórios
        base_dir = Path(__file__).parent.parent
        required_dirs = [
            base_dir / "client" / "src",
            base_dir / "server" / "src",
            base_dir / "client" / "logs",
            base_dir / "server" / "logs",
        ]
        
        for directory in required_dirs:
            if not directory.exists():
                print(f"  ❌ Diretório não encontrado: {directory}")
                return False
        
        print("  ✅ Estrutura de diretórios verificada")
        return True
        
    except ImportError as e:
        print(f"  ❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Erro inesperado: {e}")
        return False

def main():
    """Executa configuração completa"""
    print("🚀 Plante Uma Flor v2.0 - Configuração Inicial")
    print("=" * 50)
    
    steps = [
        ("Criando diretórios", create_directories),
        ("Copiando fontes", copy_fonts),
        ("Criando configurações", create_config_files),
        ("Instalando dependências", install_dependencies),
        ("Testando instalação", test_installation),
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔧 {step_name}...")
        try:
            if not step_func():
                print(f"❌ Falha em: {step_name}")
                return False
        except Exception as e:
            print(f"❌ Erro em {step_name}: {e}")
            return False
    
    print("\n" + "=" * 50)
    print("🎉 Configuração concluída com sucesso!")
    print("=" * 50)
    print("\n📋 Próximos passos:")
    print("1. Execute o servidor: python server/scripts/start_server.py")
    print("2. Execute o cliente: python client/src/main.py")
    print("3. Para build: python client/src/build/build_exe.py")
    print("4. Para testes: python scripts/test_integration.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)