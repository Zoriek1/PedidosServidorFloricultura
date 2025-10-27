#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Iniciar Servidor - Automação Flask
Este aplicativo inicia o servidor Flask automaticamente às 08:00
ou imediatamente se o computador for ligado após esse horário
"""
import subprocess
import sys
import os
import time
import webbrowser
from datetime import datetime, time as dt_time
from pathlib import Path

# Cores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

# Configurações
HORA_INICIO = dt_time(8, 0)
CHECK_INTERVAL = 60

def print_header():
    """Imprime cabeçalho da aplicação"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}  🤖 INICIAR SERVIDOR - PLANTE UMA FLOR{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_status(message, color=Colors.GREEN):
    """Imprime mensagem de status"""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {color}{message}{Colors.END}")

def server_should_run():
    """Verifica se o servidor deve estar rodando baseado no horário"""
    agora = datetime.now().time()
    return agora >= HORA_INICIO

def wait_until_start_time():
    """Aguarda até o horário de início"""
    agora = datetime.now().time()
    
    if agora >= HORA_INICIO:
        print_status(f"✓ Horário já é {agora.strftime('%H:%M')} - servidor pode iniciar")
        return True
    
    print_status(f"⏳ Aguardando até {HORA_INICIO.strftime('%H:%M')}...")
    print_status(f"   Horário atual: {agora.strftime('%H:%M')}")
    
    while True:
        agora = datetime.now().time()
        if agora >= HORA_INICIO:
            print_status(f"✓ Horário {agora.strftime('%H:%M')} alcançado!")
            return True
        time.sleep(CHECK_INTERVAL)

def start_flask_server():
    """Inicia o servidor Flask"""
    script_dir = Path(__file__).parent
    app_py = script_dir / "static" / "app.py"
    
    if not app_py.exists():
        print_status(f"❌ Erro: Arquivo não encontrado: {app_py}", Colors.RED)
        input("\nPressione Enter para sair...")
        sys.exit(1)
    
    try:
        print_status("🚀 Iniciando servidor Flask...", Colors.BLUE)
        
        process = subprocess.Popen(
            [sys.executable, str(app_py)],
            cwd=str(script_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(3)
        
        if process.poll() is not None:
            print_status("❌ Servidor Flask encerrou imediatamente!", Colors.RED)
            return None
        
        print_status("✅ Servidor Flask iniciado com sucesso!", Colors.GREEN)
        print_status(f"📋 PID: {process.pid}", Colors.BLUE)
        
        return process
        
    except Exception as e:
        print_status(f"❌ Erro ao iniciar servidor: {e}", Colors.RED)
        return None

def monitor_server(process):
    """Monitora o servidor Flask"""
    print_status("🔄 Monitoramento contínuo ativo...", Colors.YELLOW)
    print_status("   Pressione Ctrl+C para parar", Colors.YELLOW)
    print()
    
    try:
        while True:
            should_run = server_should_run()
            is_running = process is not None and process.poll() is None
            
            if should_run:
                if not is_running:
                    print_status("⚠️ Servidor não está rodando, reiniciando...", Colors.YELLOW)
                    process = start_flask_server()
            else:
                if is_running:
                    print_status("⏰ Horário de encerramento alcançado", Colors.YELLOW)
                    print_status("🛑 Parando servidor...", Colors.BLUE)
                    try:
                        process.terminate()
                        process.wait(timeout=5)
                    except:
                        process.kill()
                    process = None
                    print_status("✅ Servidor encerrado", Colors.GREEN)
            
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print_status("\n⚠️ Interrupção recebida (Ctrl+C)", Colors.YELLOW)
        
        if process:
            print_status("🛑 Encerrando servidor...", Colors.BLUE)
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()
        
        print_status("✅ Aplicação encerrada", Colors.GREEN)
        print(f"\n{Colors.BOLD}Obrigado por usar o Iniciar Servidor! 🌺{Colors.END}\n")

def main():
    """Função principal"""
    print_header()
    
    # Verificar pasta
    if not Path("static/app.py").exists():
        print_status("❌ Erro: Execute da pasta 'Servidor'", Colors.RED)
        input("\nPressione Enter para sair...")
        sys.exit(1)
    
    # Aguardar horário de início
    wait_until_start_time()
    
    # Iniciar servidor
    process = start_flask_server()
    
    # Monitorar
    monitor_server(process)

if __name__ == "__main__":
    main()

