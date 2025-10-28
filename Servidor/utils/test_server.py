# -*- coding: utf-8 -*-
"""
Script de teste do servidor
Verifica se todas as configurações estão corretas
"""
import sys
from pathlib import Path

# Adicionar diretório ao path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Testa importações"""
    print("✓ Testando importações...")
    try:
        from app import create_app, db
        from app.models import Pedido
        from app.routes import api_bp, web_bp
        from app.utils import setup_logger, NetworkDiscovery
        print("  ✓ Todas as importações OK")
        return True
    except Exception as e:
        print(f"  ✗ Erro na importação: {e}")
        return False

def test_app_creation():
    """Testa criação da aplicação"""
    print("\n✓ Testando criação da aplicação...")
    try:
        from app import create_app
        app = create_app()
        print(f"  ✓ Aplicação criada: {app.name}")
        print(f"  ✓ Blueprints registrados: {len(app.blueprints)}")
        return True, app
    except Exception as e:
        print(f"  ✗ Erro ao criar aplicação: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_database():
    """Testa banco de dados"""
    print("\n✓ Testando banco de dados...")
    try:
        from app import create_app, db
        from app.models import Pedido
        
        app = create_app()
        with app.app_context():
            # Testar consulta
            count = Pedido.query.count()
            print(f"  ✓ Banco de dados OK: {count} pedidos")
            
            # Testar estatísticas
            stats = Pedido.get_statistics()
            print(f"  ✓ Estatísticas OK: {stats}")
        return True
    except Exception as e:
        print(f"  ✗ Erro no banco de dados: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_routes():
    """Testa rotas"""
    print("\n✓ Testando rotas...")
    try:
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            # Testar página principal
            response = client.get('/')
            print(f"  ✓ Rota /: {response.status_code}")
            
            # Testar API stats
            response = client.get('/api/stats')
            print(f"  ✓ Rota /api/stats: {response.status_code}")
            
            # Testar API pedidos
            response = client.get('/api/pedidos')
            print(f"  ✓ Rota /api/pedidos: {response.status_code}")
            
        return True
    except Exception as e:
        print(f"  ✗ Erro ao testar rotas: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_network_discovery():
    """Testa network discovery"""
    print("\n✓ Testando Network Discovery...")
    try:
        from app.utils.network_discovery import NetworkDiscovery
        nd = NetworkDiscovery()
        local_ip = nd.get_local_ip()
        print(f"  ✓ IP local detectado: {local_ip}")
        return True
    except Exception as e:
        print(f"  ✗ Erro no Network Discovery: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("=" * 50)
    print("  TESTE DO SERVIDOR - Plante Uma Flor v2.0")
    print("=" * 50)
    print()
    
    tests = [
        test_imports,
        test_app_creation,
        test_database,
        test_routes,
        test_network_discovery
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            if isinstance(result, tuple):
                result = result[0]
            results.append(result)
        except Exception as e:
            print(f"\n✗ Erro inesperado: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✓ TODOS OS TESTES PASSARAM ({passed}/{total})")
        print("\nServidor pronto para iniciar!")
        print("Execute: python main.py")
    else:
        print(f"✗ ALGUNS TESTES FALHARAM ({passed}/{total})")
        print("\nCorreja os erros acima antes de iniciar o servidor.")
    
    print("=" * 50)
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

