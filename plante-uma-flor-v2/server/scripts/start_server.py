# -*- coding: utf-8 -*-
"""
Script de inicialização do servidor
"""
import os
import sys
import subprocess
from pathlib import Path

def start_server():
    """Inicia o servidor com configurações otimizadas"""
    
    # Caminhos
    server_dir = Path(__file__).parent.parent
    src_dir = server_dir / "src"
    
    print("🚀 Iniciando Plante Uma Flor v2.0 - Servidor Web")
    print("=" * 50)
    
    # Verificar se Python está disponível
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✅ Python: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Erro ao verificar Python: {e}")
        return False
    
    # Verificar dependências
    try:
        import flask
        import flask_sqlalchemy
        print("✅ Dependências Flask verificadas")
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        return False
    
    # Configurar variáveis de ambiente
    os.environ.setdefault('FLASK_APP', 'main.py')
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ.setdefault('HOST', '0.0.0.0')
    os.environ.setdefault('PORT', '5000')
    
    # Criar diretórios necessários
    logs_dir = server_dir / "logs"
    database_dir = server_dir / "database"
    
    logs_dir.mkdir(exist_ok=True)
    database_dir.mkdir(exist_ok=True)
    
    print(f"📁 Logs: {logs_dir}")
    print(f"📁 Database: {database_dir}")
    
    # Iniciar servidor
    try:
        print("\n🌐 Servidor iniciando...")
        print("🔒 Modo de segurança: Criação via web BLOQUEADA")
        print("📱 Apenas aplicativo desktop pode criar pedidos")
        print("\n" + "=" * 50)
        
        # Executar servidor
        subprocess.run([
            sys.executable, "main.py"
        ], cwd=src_dir)
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Servidor interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_server()