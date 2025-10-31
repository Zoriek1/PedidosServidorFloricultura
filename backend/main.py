# -*- coding: utf-8 -*-
"""
Plante Uma Flor v3.0 - PWA
Inicialização do servidor Flask
"""
import os
import sys
import configparser
from pathlib import Path

# Configurar encoding UTF-8 para evitar erros no Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from app import create_app
from app.config import config

def get_local_ip():
    """Descobre o IP local da máquina"""
    import socket
    try:
        # Conecta a um endereço externo para descobrir IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "192.168.1.148"  # Fallback

def get_hostname():
    """Lê o hostname configurado do arquivo config_servidor.ini"""
    config_file = Path(__file__).parent / 'config_servidor.ini'
    
    if not config_file.exists():
        return "Gestor-pedidos.local"  # Padrão
    
    try:
        parser = configparser.ConfigParser()
        parser.read(config_file, encoding='utf-8')
        hostname = parser.get('SERVIDOR', 'hostname', fallback='Gestor-pedidos.local')
        return hostname.strip()
    except:
        return "Gestor-pedidos.local"  # Fallback em caso de erro

def check_ssl_certificates():
    """Verifica se os certificados SSL existem"""
    ssl_dir = Path(__file__).parent / 'ssl'
    cert_file = ssl_dir / 'cert.pem'
    key_file = ssl_dir / 'key.pem'
    
    if cert_file.exists() and key_file.exists():
        return (str(cert_file), str(key_file))
    return None

def check_port_in_use(port=5000):
    """Verifica se a porta já está em uso"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0
    except:
        return False

def main():
    """Função principal para iniciar o servidor"""
    
    # Verificar se a porta já está em uso
    if check_port_in_use(5000):
        print("\n[AVISO] A porta 5000 ja esta em uso!")
        print("   Servidor pode ja estar rodando.")
        print("   Para parar: Execute parar_servidor.bat")
        print("   Ou tente acessar: https://localhost:5000\n")
        
        resposta = input("Deseja tentar iniciar mesmo assim? (s/n): ")
        if resposta.lower() != 's':
            print("\n[INFO] Inicializacao cancelada.")
            return
    
    # Determinar ambiente (development ou production)
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Verificar modo HTTPS
    use_https = '--https' in sys.argv or os.environ.get('USE_HTTPS', '').lower() == 'true'
    
    # Verificar se deve desativar reloader (para evitar problemas)
    no_reload = '--no-reload' in sys.argv or os.environ.get('NO_RELOAD', '').lower() == 'true'
    
    # Criar aplicação com configuração apropriada
    app_config = config.get(env, config['default'])
    app = create_app(config={
        'SECRET_KEY': app_config.SECRET_KEY,
        'SQLALCHEMY_DATABASE_URI': app_config.SQLALCHEMY_DATABASE_URI,
        'SQLALCHEMY_TRACK_MODIFICATIONS': app_config.SQLALCHEMY_TRACK_MODIFICATIONS,
        'JSON_AS_ASCII': app_config.JSON_AS_ASCII,
        'JSON_SORT_KEYS': app_config.JSON_SORT_KEYS
    })
    
    # Descobrir IP local e hostname
    local_ip = get_local_ip()
    hostname = get_hostname()
    
    # Configurar SSL
    ssl_context = None
    protocol = "http"
    
    if use_https:
        ssl_certs = check_ssl_certificates()
        if ssl_certs:
            ssl_context = ssl_certs
            protocol = "https"
            print("\n[HTTPS] Modo HTTPS ativado!")
        else:
            print("\n[AVISO] Modo HTTPS solicitado mas certificados nao encontrados!")
            print("   Execute: ssl/GERAR_CERTIFICADOS.bat")
            print("   Iniciando em HTTP...\n")
    
    # Informações de inicialização
    print("\n" + "="*60)
    print("PLANTE UMA FLOR - PWA v3.0")
    print("="*60)
    print(f"Ambiente: {env}")
    print(f"Protocolo: {protocol.upper()}")
    print(f"Host: {app_config.HOST}")
    print(f"Porta: {app_config.PORT}")
    
    # Mostrar status do debug baseado no que será usado
    debug_status = "OFF (estavel)" if no_reload else app_config.DEBUG
    print(f"Debug: {debug_status}")
    print(f"Banco de dados: {app_config.DATABASE_PATH}")
    
    if ssl_context:
        print(f"Certificados SSL: [OK] Configurados")
    
    print("\nServidor acessivel em:")
    print(f"   Local:    {protocol}://localhost:{app_config.PORT}")
    print(f"   Hostname: {protocol}://{hostname}:{app_config.PORT}")
    print(f"   IP Rede:  {protocol}://{local_ip}:{app_config.PORT}")
    
    if protocol == "https":
        print("\n[INFO] PWA pode ser instalado em todos os dispositivos!")
        print("   Acesse via HTTPS e clique no botao de instalar")
    else:
        print("\n[AVISO] Modo HTTP: PWA so instala em localhost")
        print("   Para instalar em outros dispositivos, use HTTPS:")
        print("   1. Execute: ssl/GERAR_CERTIFICADOS.bat")
        print("   2. Inicie com: iniciar_servidor_https.bat")
    
    # Configurar opções de execução
    run_options = {
        'host': app_config.HOST,
        'port': app_config.PORT,
        'ssl_context': ssl_context
    }
    
    # Desativar reloader se solicitado (evita problemas de "travamento")
    if no_reload:
        # Desativar completamente debug e reloader para modo estável
        run_options['debug'] = False
        run_options['use_reloader'] = False
        print("\n[INFO] Modo estavel: Debug e reloader desativados")
    else:
        # Modo debug normal (com reloader)
        run_options['debug'] = app_config.DEBUG
        run_options['use_reloader'] = True
    
    print("\n[OK] Pressione Ctrl+C para parar o servidor")
    print("="*60 + "\n")
    
    # Iniciar servidor
    try:
        app.run(**run_options)
    except KeyboardInterrupt:
        print("\n\n[AVISO] Servidor encerrado pelo usuario")
        print("[OK] Obrigado por usar Plante Uma Flor!\n")
    except Exception as e:
        print(f"\n[ERRO] Erro ao iniciar servidor: {e}\n")
        raise

if __name__ == '__main__':
    main()

