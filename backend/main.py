# -*- coding: utf-8 -*-
"""
Plante Uma Flor v3.0 - PWA
Inicialização do servidor Flask
"""
import os
import sys
from pathlib import Path
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

def check_ssl_certificates():
    """Verifica se os certificados SSL existem"""
    ssl_dir = Path(__file__).parent / 'ssl'
    cert_file = ssl_dir / 'cert.pem'
    key_file = ssl_dir / 'key.pem'
    
    if cert_file.exists() and key_file.exists():
        return (str(cert_file), str(key_file))
    return None

def main():
    """Função principal para iniciar o servidor"""
    
    # Determinar ambiente (development ou production)
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Verificar modo HTTPS
    use_https = '--https' in sys.argv or os.environ.get('USE_HTTPS', '').lower() == 'true'
    
    # Criar aplicação com configuração apropriada
    app_config = config.get(env, config['default'])
    app = create_app(config={
        'SECRET_KEY': app_config.SECRET_KEY,
        'SQLALCHEMY_DATABASE_URI': app_config.SQLALCHEMY_DATABASE_URI,
        'SQLALCHEMY_TRACK_MODIFICATIONS': app_config.SQLALCHEMY_TRACK_MODIFICATIONS,
        'JSON_AS_ASCII': app_config.JSON_AS_ASCII,
        'JSON_SORT_KEYS': app_config.JSON_SORT_KEYS
    })
    
    # Descobrir IP local
    local_ip = get_local_ip()
    
    # Configurar SSL
    ssl_context = None
    protocol = "http"
    
    if use_https:
        ssl_certs = check_ssl_certificates()
        if ssl_certs:
            ssl_context = ssl_certs
            protocol = "https"
            print("\n🔒 Modo HTTPS ativado!")
        else:
            print("\n⚠️  AVISO: Modo HTTPS solicitado mas certificados não encontrados!")
            print("   Execute: ssl/GERAR_CERTIFICADOS.bat")
            print("   Iniciando em HTTP...\n")
    
    # Informações de inicialização
    print("\n" + "="*60)
    print("🌺 PLANTE UMA FLOR - PWA v3.0")
    print("="*60)
    print(f"Ambiente: {env}")
    print(f"Protocolo: {protocol.upper()}")
    print(f"Host: {app_config.HOST}")
    print(f"Porta: {app_config.PORT}")
    print(f"Debug: {app_config.DEBUG}")
    print(f"Banco de dados: {app_config.DATABASE_PATH}")
    
    if ssl_context:
        print(f"Certificados SSL: ✅ Configurados")
    
    print("\n📡 Servidor acessível em:")
    print(f"   Local: {protocol}://localhost:{app_config.PORT}")
    print(f"   Rede: {protocol}://{local_ip}:{app_config.PORT}")
    
    if protocol == "https":
        print("\n🎉 PWA pode ser instalado em todos os dispositivos!")
        print("   Acesse via HTTPS e clique no botão de instalar")
    else:
        print("\n⚠️  Modo HTTP: PWA só instala em localhost")
        print("   Para instalar em outros dispositivos, use HTTPS:")
        print("   1. Execute: ssl/GERAR_CERTIFICADOS.bat")
        print("   2. Inicie com: iniciar_servidor_https.bat")
    
    print("\n✅ Pressione Ctrl+C para parar o servidor")
    print("="*60 + "\n")
    
    # Iniciar servidor
    try:
        app.run(
            host=app_config.HOST,
            port=app_config.PORT,
            debug=app_config.DEBUG,
            ssl_context=ssl_context
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Servidor encerrado pelo usuário")
        print("✅ Obrigado por usar Plante Uma Flor! 🌺\n")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}\n")
        raise

if __name__ == '__main__':
    main()

