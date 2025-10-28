# -*- coding: utf-8 -*-
"""
Script de teste para descoberta automática de rede
Execute antes de compilar para verificar se funciona
"""
import socket
import json
import time
import requests

def descobrir_servidor():
    """Descobre servidor Flask automaticamente via UDP broadcast"""
    print("🔍 Procurando servidor na rede...")
    print("=" * 60)
    
    try:
        # Tentar descoberta via broadcast UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 37020))  # Porta do broadcast
        sock.settimeout(10)  # Timeout de 10 segundos
        
        print("📡 Escutando broadcasts UDP na porta 37020...")
        print("⏱️  Aguardando até 10 segundos...")
        print()
        
        start_time = time.time()
        while time.time() - start_time < 10:
            try:
                data, addr = sock.recvfrom(1024)
                message = json.loads(data.decode('utf-8'))
                
                print(f"📦 Broadcast recebido de {addr}:")
                print(f"   {message}")
                print()
                
                if message.get('service') == 'plante-uma-flor-server':
                    server_url = f"http://{message['ip']}:{message['port']}"
                    print(f"✅ SERVIDOR ENCONTRADO VIA BROADCAST!")
                    print(f"   URL: {server_url}")
                    print(f"   IP: {message['ip']}")
                    print(f"   Porta: {message['port']}")
                    sock.close()
                    return server_url
                    
            except socket.timeout:
                break
            except Exception as e:
                print(f"⚠️  Erro ao processar broadcast: {e}")
                continue
                
        sock.close()
        print("⏱️  Timeout: Nenhum broadcast recebido")
        print()
        
    except Exception as e:
        print(f"❌ Erro no socket UDP: {e}")
        print()
    
    # Fallback: tentar IPs comuns
    print("🔄 Tentando IPs comuns da rede...")
    print("-" * 60)
    
    fallback_ips = [
        "192.168.1.148",
        "192.168.1.100", 
        "192.168.1.101",
        "192.168.0.100",
        "192.168.0.101",
        "localhost",
        "127.0.0.1"
    ]
    
    for ip in fallback_ips:
        try:
            url = f"http://{ip}:5000"
            print(f"   Testando: {url} ... ", end="")
            response = requests.get(f"{url}/api/stats", timeout=2)
            if response.status_code == 200:
                print("✅ ENCONTRADO!")
                print()
                print(f"✅ SERVIDOR ENCONTRADO VIA FALLBACK!")
                print(f"   URL: {url}")
                return url
            else:
                print(f"❌ Status {response.status_code}")
        except Exception:
            print("❌ Falhou")
            continue
    
    print()
    print("=" * 60)
    print("❌ SERVIDOR NÃO ENCONTRADO!")
    print()
    print("Verifique:")
    print("  1. O servidor está rodando? (Servidor/INICIAR_AQUI.bat)")
    print("  2. Está na mesma rede?")
    print("  3. Firewall bloqueando portas 5000 (TCP) e 37020 (UDP)?")
    print("=" * 60)
    return None

def testar_api(server_url):
    """Testa a API do servidor"""
    if not server_url:
        return
    
    print()
    print("=" * 60)
    print("🧪 TESTANDO API DO SERVIDOR")
    print("=" * 60)
    
    try:
        # Testar /api/stats
        print(f"\n📊 GET {server_url}/api/stats")
        response = requests.get(f"{server_url}/api/stats", timeout=5)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Resposta: {data}")
            print("   ✅ API funcionando!")
        else:
            print(f"   ❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")

if __name__ == "__main__":
    print()
    print("=" * 60)
    print("  TESTE DE DESCOBERTA AUTOMÁTICA DE REDE")
    print("  Plante Uma Flor v2.0")
    print("=" * 60)
    print()
    
    server_url = descobrir_servidor()
    
    if server_url:
        testar_api(server_url)
        print()
        print("=" * 60)
        print("✅ SISTEMA PRONTO PARA COMPILAÇÃO!")
        print("=" * 60)
        print()
        print("Execute: COMPILAR.bat")
    else:
        print()
        print("⚠️  Inicie o servidor primeiro e tente novamente.")
    
    print()
    input("Pressione ENTER para sair...")

