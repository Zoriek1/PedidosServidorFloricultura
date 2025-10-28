# -*- coding: utf-8 -*-
"""
Script de teste para validar as correções realizadas
"""
import sys
from pathlib import Path

def test_server_imports():
    """Testa se o servidor pode ser importado sem erros"""
    print("🔍 Testando imports do servidor...")
    try:
        sys.path.insert(0, str(Path(__file__).parent / 'server' / 'src'))
        from app import create_app
        app = create_app()
        print("✅ Servidor: Imports OK")
        print(f"   - Template folder: {app.template_folder}")
        print(f"   - Static folder: {app.static_folder}")
        return True
    except Exception as e:
        print(f"❌ Servidor: Erro ao importar - {e}")
        return False

def test_client_imports():
    """Testa se o cliente pode ser importado sem erros"""
    print("\n🔍 Testando imports do cliente...")
    try:
        sys.path.insert(0, str(Path(__file__).parent / 'client' / 'src'))
        
        # Testar imports críticos
        from app.gui.main_window import MainWindow
        from app.core.pdf_generator import PDFGenerator
        from app.core.api_client import APIClient
        from app.core.database import DatabaseManager
        
        print("✅ Cliente: Imports OK")
        print("   - MainWindow: OK")
        print("   - PDFGenerator: OK")
        print("   - APIClient: OK")
        print("   - DatabaseManager: OK")
        return True
    except Exception as e:
        print(f"❌ Cliente: Erro ao importar - {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🧪 TESTE DE VALIDAÇÃO DAS CORREÇÕES")
    print("=" * 60)
    
    results = []
    
    # Teste 1: Servidor
    results.append(("Servidor", test_server_imports()))
    
    # Teste 2: Cliente
    results.append(("Cliente", test_client_imports()))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O projeto está pronto para uso")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("❌ Verifique os erros acima")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

