# -*- coding: utf-8 -*-
"""
Script de teste de integração completa
"""
import sys
import os
import time
import subprocess
import requests
from pathlib import Path
from datetime import datetime

def test_client_build():
    """Testa build do cliente"""
    print("🔨 Testando build do cliente...")
    
    client_dir = Path(__file__).parent.parent / "client"
    build_script = client_dir / "src" / "build" / "build_exe.py"
    
    try:
        result = subprocess.run([
            sys.executable, str(build_script)
        ], cwd=client_dir, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Build do cliente executado com sucesso")
            return True
        else:
            print(f"❌ Erro no build do cliente: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout no build do cliente")
        return False
    except Exception as e:
        print(f"❌ Erro ao executar build: {e}")
        return False

def test_server_startup():
    """Testa inicialização do servidor"""
    print("🌐 Testando inicialização do servidor...")
    
    server_dir = Path(__file__).parent.parent / "server"
    start_script = server_dir / "scripts" / "start_server.py"
    
    try:
        # Iniciar servidor em background
        process = subprocess.Popen([
            sys.executable, str(start_script)
        ], cwd=server_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Aguardar inicialização
        time.sleep(5)
        
        # Testar conexão
        try:
            response = requests.get("http://localhost:5000/", timeout=5)
            if response.status_code == 200:
                print("✅ Servidor iniciado com sucesso")
                process.terminate()
                return True
            else:
                print(f"❌ Servidor retornou status {response.status_code}")
                process.terminate()
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao conectar com servidor: {e}")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        return False

def test_api_endpoints():
    """Testa endpoints da API"""
    print("🔌 Testando endpoints da API...")
    
    base_url = "http://localhost:5000"
    
    try:
        # Testar endpoint principal
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code != 200:
            print(f"❌ Endpoint principal falhou: {response.status_code}")
            return False
        
        # Testar listagem de pedidos
        response = requests.get(f"{base_url}/api/pedidos", timeout=5)
        if response.status_code != 200:
            print(f"❌ Endpoint de pedidos falhou: {response.status_code}")
            return False
        
        print("✅ Endpoints da API funcionando")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao testar API: {e}")
        return False

def test_security():
    """Testa medidas de segurança"""
    print("🔒 Testando medidas de segurança...")
    
    base_url = "http://localhost:5000"
    
    try:
        # Tentar criar pedido via web (deve falhar)
        response = requests.post(f"{base_url}/criar-pedido", timeout=5)
        if response.status_code == 403:
            print("✅ Criação via web bloqueada corretamente")
        else:
            print(f"❌ Criação via web não está bloqueada: {response.status_code}")
            return False
        
        # Tentar criar pedido via API sem autenticação (deve falhar)
        response = requests.post(f"{base_url}/api/pedidos", json={}, timeout=5)
        if response.status_code == 401:
            print("✅ API requer autenticação")
        else:
            print(f"❌ API não requer autenticação: {response.status_code}")
            return False
        
        print("✅ Medidas de segurança funcionando")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao testar segurança: {e}")
        return False

def test_database():
    """Testa banco de dados"""
    print("🗄️ Testando banco de dados...")
    
    server_dir = Path(__file__).parent.parent / "server"
    db_path = server_dir / "database" / "pedidos.db"
    
    if db_path.exists():
        print("✅ Banco de dados criado")
        return True
    else:
        print("❌ Banco de dados não encontrado")
        return False

def test_logs():
    """Testa sistema de logs"""
    print("📝 Testando sistema de logs...")
    
    client_logs = Path(__file__).parent.parent / "client" / "logs"
    server_logs = Path(__file__).parent.parent / "server" / "logs"
    
    if client_logs.exists() and server_logs.exists():
        print("✅ Diretórios de logs criados")
        return True
    else:
        print("❌ Diretórios de logs não encontrados")
        return False

def main():
    """Executa todos os testes"""
    print("🧪 Plante Uma Flor v2.0 - Teste de Integração")
    print("=" * 50)
    
    tests = [
        ("Banco de Dados", test_database),
        ("Sistema de Logs", test_logs),
        ("Build do Cliente", test_client_build),
        ("Inicialização do Servidor", test_server_startup),
        ("Endpoints da API", test_api_endpoints),
        ("Medidas de Segurança", test_security),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            results.append((test_name, False))
    
    # Resumo dos resultados
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Sistema pronto para uso.")
        return True
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)