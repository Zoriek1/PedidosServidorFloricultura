# -*- coding: utf-8 -*-
"""
Plante Uma Flor v2.0 - Servidor Principal
Entry point da aplicação
"""
import os
import sys
from pathlib import Path

# Adicionar diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from app.config import Config
from app.utils.logger import setup_logger
from app.utils.network_discovery import NetworkDiscovery

def main():
    """Entry point principal do servidor"""
    logger = setup_logger(__name__)
    
    try:
        logger.info("=" * 60)
        logger.info("Iniciando Plante Uma Flor v2.0 - Servidor de Pedidos")
        logger.info("=" * 60)
        
        # Carregar configurações
        config_data = Config.load_from_file('config.json')
        
        # Criar configuração padrão se não existir
        if not config_data:
            logger.info("Criando arquivo de configuração padrão...")
            config_data = Config.create_default_config()
            Config.save_to_file(config_data, 'config.json')
        
        # Extrair configurações
        server_config = config_data.get('server', {})
        host = server_config.get('host', '0.0.0.0')
        port = server_config.get('port', 5000)
        debug = server_config.get('debug', False)
        broadcast_enabled = server_config.get('broadcast_enabled', True)
        broadcast_port = server_config.get('broadcast_port', 37020)
        broadcast_interval = server_config.get('broadcast_interval', 5)
        
        # Criar aplicação Flask
        logger.info("Criando aplicação Flask...")
        app = create_app(config=server_config)
        
        # Iniciar Network Discovery se habilitado
        network_discovery = None
        if broadcast_enabled:
            logger.info("Iniciando sistema de descoberta de rede (UDP Broadcast)...")
            network_discovery = NetworkDiscovery(
                port=port,
                broadcast_port=broadcast_port,
                interval=broadcast_interval
            )
            network_discovery.start()
            logger.info(f"Broadcast habilitado na porta UDP {broadcast_port}")
        
        # Informações de inicialização
        logger.info(f"Servidor configurado:")
        logger.info(f"  - Host: {host}")
        logger.info(f"  - Porta: {port}")
        logger.info(f"  - Debug: {debug}")
        logger.info(f"  - Broadcast: {'Habilitado' if broadcast_enabled else 'Desabilitado'}")
        
        if host == '0.0.0.0':
            # Mostrar IP local para facilitar conexão
            nd_temp = NetworkDiscovery()
            local_ip = nd_temp.get_local_ip()
            logger.info(f"\nServidor acessível em:")
            logger.info(f"  - Local: http://localhost:{port}")
            logger.info(f"  - Rede: http://{local_ip}:{port}")
            logger.info(f"\nClientes PDFgen.py podem se conectar automaticamente!")
        
        logger.info("\nServidor Flask iniciando...")
        logger.info("Pressione Ctrl+C para parar\n")
        
        # Iniciar servidor Flask
        try:
            app.run(
                host=host,
                port=port,
                debug=debug,
                use_reloader=False  # Evita problemas com threads de broadcast
            )
        except KeyboardInterrupt:
            logger.info("\nServidor interrompido pelo usuário")
        finally:
            # Parar network discovery
            if network_discovery:
                logger.info("Parando sistema de descoberta de rede...")
                network_discovery.stop()
        
        logger.info("Servidor encerrado com sucesso")
        
    except Exception as e:
        logger.error(f"Erro fatal ao iniciar servidor: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()

