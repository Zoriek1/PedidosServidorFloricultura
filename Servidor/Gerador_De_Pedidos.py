#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gerador de Pedidos - Servidor Flask
Este aplicativo roda o servidor Flask e monitora continuamente
"""
import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def get_base_path():
    """Retorna o caminho base, funcionando tanto compilado quanto em desenvolvimento"""
    if getattr(sys, 'frozen', False):
        # Executável compilado - PyInstaller cria uma pasta temporária
        # O executável procura os arquivos na mesma pasta
        base_path = Path(sys.executable).parent
    else:
        # Desenvolvimento (script Python)
        base_path = Path(__file__).parent
    return base_path

# Cores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Imprime cabeçalho da aplicação"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}  🌺 GERADOR DE PEDIDOS - PLANTE UMA FLOR{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_status(message, color=Colors.GREEN):
    """Imprime mensagem de status"""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {color}{message}{Colors.END}")

def start_flask_server():
    """Inicia o servidor Flask"""
    # Caminho para o app.py
    base_path = get_base_path()
    app_py = base_path / "static" / "app.py"
    
    if not app_py.exists():
        print_status(f"❌ Erro: Arquivo não encontrado: {app_py}", Colors.RED)
        input("\nPressione Enter para sair...")
        sys.exit(1)
    
    try:
        print_status("🚀 Iniciando servidor Flask...", Colors.BLUE)
        
        # Iniciar processo Flask
        process = subprocess.Popen(
            [sys.executable, str(app_py)],
            cwd=str(base_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Aguardar um momento para verificar se iniciou corretamente
        time.sleep(3)
        
        if process.poll() is not None:
            print_status("❌ Servidor Flask encerrou imediatamente!", Colors.RED)
            stdout, stderr = process.communicate(timeout=2)
            print(f"\nErro: {stderr}", Colors.RED)
            input("\nPressione Enter para sair...")
            sys.exit(1)
        
        print_status("✅ Servidor Flask iniciado com sucesso!", Colors.GREEN)
        print_status(f"📋 PID do processo: {process.pid}", Colors.BLUE)
        print_status(f"🌐 URL: http://localhost:5000", Colors.BLUE)
        print_status(f"🌐 URL Rede: http://192.168.1.148:5000", Colors.BLUE)
        
        return process
        
    except Exception as e:
        print_status(f"❌ Erro ao iniciar servidor: {e}", Colors.RED)
        input("\nPressione Enter para sair...")
        sys.exit(1)

def start_pdfgen():
    """Inicia o Gerador de Pedidos (PDFgen)"""
    base_path = get_base_path()
    parent_dir = base_path.parent
    
    # Procurar PDFgen.exe na pasta Clientes
    pdfgen_exe = parent_dir / "Clientes" / "PDFgen.exe"
    
    # Se não encontrar .exe, procura o .py
    if not pdfgen_exe.exists():
        pdfgen_py = parent_dir / "Clientes" / "PDFgen.py"
        if pdfgen_py.exists():
            # Usar o .py diretamente
            pdfgen_exe = pdfgen_py
    
    if not pdfgen_exe.exists():
        print_status("⚠️ PDFgen não encontrado, tentando executar PDFgen.py...", Colors.YELLOW)
        
        # Tentar executar PDFgen.py diretamente
        pdfgen_py = parent_dir / "Clientes" / "PDFgen.py"
        if pdfgen_py.exists():
            try:
                print_status("📄 Iniciando PDFgen.py...", Colors.BLUE)
                subprocess.Popen(
                    [sys.executable, str(pdfgen_py)],
                    cwd=str(parent_dir / "Clientes"),
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
                print_status("✅ PDFgen iniciado!", Colors.GREEN)
                return True
            except Exception as e:
                print_status(f"⚠️ Erro ao iniciar PDFgen: {e}", Colors.YELLOW)
                return False
        else:
            print_status("❌ PDFgen não encontrado!", Colors.RED)
            return False
    
    try:
        print_status("📄 Iniciando Gerador de Pedidos (PDFgen)...", Colors.BLUE)
        
        # Executar PDFgen.exe em nova janela
        subprocess.Popen(
            [str(pdfgen_exe)],
            cwd=str(pdfgen_exe.parent),
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        
        print_status("✅ Gerador de Pedidos iniciado!", Colors.GREEN)
        return True
        
    except Exception as e:
        print_status(f"⚠️ Erro ao iniciar PDFgen: {e}", Colors.YELLOW)
        return False

def monitor_server(process):
    """Monitora o servidor Flask e reinicia se necessário"""
    print_status("🔄 Monitoramento ativo...", Colors.YELLOW)
    print_status("   Pressione Ctrl+C para parar o servidor", Colors.YELLOW)
    print()
    
    # Abrir navegador automaticamente
    try:
        webbrowser.open('http://localhost:5000')
        print_status("🌐 Navegador aberto automaticamente", Colors.GREEN)
    except:
        pass
    
    try:
        while True:
            # Verificar se o processo ainda está rodando
            if process.poll() is not None:
                exit_code = process.returncode
                print_status(f"⚠️ Servidor Flask encerrou (código: {exit_code})", Colors.YELLOW)
                print_status("🔄 Reiniciando servidor...", Colors.BLUE)
                
                # Reiniciar o servidor
                process = start_flask_server()
                time.sleep(2)
            
            # Aguardar antes da próxima verificação
            time.sleep(5)
            
    except KeyboardInterrupt:
        print_status("\n⚠️ Interrupção recebida (Ctrl+C)", Colors.YELLOW)
        print_status("🛑 Encerrando servidor Flask...", Colors.BLUE)
        
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()
        
        print_status("✅ Aplicação encerrada", Colors.GREEN)
        print(f"\n{Colors.BOLD}Obrigado por usar o Gerador de Pedidos! 🌺{Colors.END}\n")

def main():
    """Função principal"""
    print_header()
    
    # Verificar se está na pasta correta
    base_path = get_base_path()
    app_py = base_path / "static" / "app.py"
    
    if not app_py.exists():
        print_status(f"❌ Erro: Arquivo não encontrado: {app_py}", Colors.RED)
        print_status("   Certifique-se de que os arquivos estão no lugar correto", Colors.YELLOW)
        input("\nPressione Enter para sair...")
        sys.exit(1)
    
    # Iniciar servidor Flask
    process = start_flask_server()
    
    # Iniciar Gerador de Pedidos (PDFgen)
    start_pdfgen()
    
    print()
    print_status("="*60, Colors.BLUE)
    print_status("Sistema completo inicializado!", Colors.GREEN)
    print_status("  - Servidor Flask rodando em http://localhost:5000", Colors.BLUE)
    print_status("  - Gerador de Pedidos aberto", Colors.BLUE)
    print_status("="*60, Colors.BLUE)
    print()
    
    # Monitorar servidor
    monitor_server(process)

if __name__ == "__main__":
    main()

