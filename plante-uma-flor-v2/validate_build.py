# -*- coding: utf-8 -*-
"""
Script de validação para verificar se o projeto está pronto para build
"""
import sys
import os
from pathlib import Path

# Configurar encoding para Windows
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
    sys.stderr.reconfigure(encoding='utf-8', errors='ignore')

def validate_client_structure():
    """Valida estrutura do cliente"""
    print("[*] Validando estrutura do cliente...")
    print("=" * 60)
    
    client_root = Path(__file__).parent / "client"
    src_dir = client_root / "src"
    
    required_files = [
        src_dir / "main.py",
        src_dir / "app" / "__init__.py",
        src_dir / "app" / "core" / "database.py",
        src_dir / "app" / "core" / "api_client.py",
        src_dir / "app" / "core" / "pdf_generator.py",
        src_dir / "app" / "gui" / "main_window.py",
        src_dir / "app" / "gui" / "forms" / "pedido_form.py",
        src_dir / "app" / "utils" / "logger.py",
        src_dir / "app" / "utils" / "fonts.py",
        src_dir / "resources" / "config.json",
        src_dir / "build" / "build_complete.py",
    ]
    
    missing = []
    for file_path in required_files:
        if file_path.exists():
            print(f"  [OK] {file_path.relative_to(client_root)}")
        else:
            print(f"  [ERRO] {file_path.relative_to(client_root)} - FALTANDO")
            missing.append(file_path)
    
    if missing:
        print(f"\n[ERRO] {len(missing)} arquivos faltando!")
        return False
    
    print("\n[OK] Estrutura do cliente OK!\n")
    return True

def test_imports():
    """Testa imports principais"""
    print("[*] Testando imports...")
    print("=" * 60)
    
    # Adicionar ao path
    src_dir = Path(__file__).parent / "client" / "src"
    sys.path.insert(0, str(src_dir))
    
    test_cases = [
        ("tkinter", "Tkinter (GUI)"),
        ("sqlite3", "SQLite3 (Database)"),
        ("pathlib", "Pathlib"),
        ("datetime", "Datetime"),
        ("typing", "Typing"),
        ("json", "JSON"),
    ]
    
    optional_deps = [
        ("reportlab", "ReportLab (PDF)"),
        ("requests", "Requests (HTTP)"),
        ("PyInstaller", "PyInstaller (Build)"),
    ]
    
    all_ok = True
    
    print("\n[*] Dependencias principais:")
    for module, name in test_cases:
        try:
            __import__(module)
            print(f"  [OK] {name}")
        except ImportError:
            print(f"  [ERRO] {name} - NAO ENCONTRADO")
            all_ok = False
    
    print("\n[*] Dependencias opcionais (para build):")
    build_ready = True
    for module, name in optional_deps:
        try:
            __import__(module)
            print(f"  [OK] {name}")
        except ImportError:
            print(f"  [AVISO] {name} - NAO ENCONTRADO (necessario para build)")
            build_ready = False
    
    if not build_ready:
        print("\n[INFO] Para instalar dependencias de build:")
        print("   pip install reportlab requests pyinstaller")
    
    print()
    return all_ok

def test_application_imports():
    """Testa imports da aplicação"""
    print("[*] Testando imports da aplicacao...")
    print("=" * 60)
    
    src_dir = Path(__file__).parent / "client" / "src"
    sys.path.insert(0, str(src_dir))
    
    app_imports = [
        ("app.core.database", "DatabaseManager"),
        ("app.core.api_client", "APIClient"),
        ("app.core.pdf_generator", "PDFGenerator"),
        ("app.utils.logger", "Logger"),
        ("app.utils.fonts", "FontManager"),
    ]
    
    all_ok = True
    for module, name in app_imports:
        try:
            __import__(module)
            print(f"  [OK] {name} ({module})")
        except Exception as e:
            print(f"  [ERRO] {name} ({module}) - ERRO: {e}")
            all_ok = False
    
    if all_ok:
        print("\n[OK] Todos os imports da aplicacao estao OK!\n")
    else:
        print("\n[ERRO] Alguns imports falharam!\n")
    
    return all_ok

def check_build_scripts():
    """Verifica scripts de build"""
    print("[*] Verificando scripts de build...")
    print("=" * 60)
    
    build_dir = Path(__file__).parent / "client" / "src" / "build"
    
    build_scripts = [
        ("build_complete.py", "Build Completo (RECOMENDADO)"),
        ("build_simple.py", "Build Simplificado"),
        ("build_exe.py", "Build com Nuitka"),
        ("requirements.txt", "Dependências"),
    ]
    
    available_scripts = []
    for script, desc in build_scripts:
        script_path = build_dir / script
        if script_path.exists():
            print(f"  [OK] {desc} ({script})")
            available_scripts.append(script)
        else:
            print(f"  [AVISO] {desc} ({script}) - nao encontrado")
    
    print(f"\n[OK] {len(available_scripts)} scripts disponiveis\n")
    return len(available_scripts) > 0

def generate_report():
    """Gera relatório final"""
    print("=" * 60)
    print("RELATORIO FINAL")
    print("=" * 60)
    
    validations = [
        ("Estrutura do Cliente", validate_client_structure),
        ("Imports do Sistema", test_imports),
        ("Imports da Aplicação", test_application_imports),
        ("Scripts de Build", check_build_scripts),
    ]
    
    results = []
    for name, func in validations:
        try:
            result = func()
            results.append((name, result))
        except Exception as e:
            print(f"[ERRO] Erro em {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    
    for name, result in results:
        status = "[OK] PASSOU" if result else "[ERRO] FALHOU"
        print(f"{name}: {status}")
    
    all_passed = all(r[1] for r in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("VALIDACAO COMPLETA!")
        print("[OK] Projeto pronto para build")
        print("\n[INFO] Para fazer o build, execute:")
        print("   cd plante-uma-flor-v2\\client\\src\\build")
        print("   python build_complete.py")
    else:
        print("[AVISO] VALIDACAO COM ERROS")
        print("[ERRO] Corrija os erros antes de fazer o build")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    try:
        success = generate_report()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERRO FATAL] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

