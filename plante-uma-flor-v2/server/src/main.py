# -*- coding: utf-8 -*-
"""
Plante Uma Flor v2.0 - Servidor Web
Entry point otimizado com segurança
"""
import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from app.utils.logger import setup_logger

def main():
    """Entry point principal do servidor"""
    logger = setup_logger(__name__)
    
    try:
        logger.info("Iniciando Plante Uma Flor v2.0 - Servidor Web")
        
        # Criar aplicação
        app = create_app()
        
        # Configurações do servidor
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('DEBUG', 'False').lower() == 'true'
        
        logger.info(f"Servidor iniciando em {host}:{port}")
        logger.info("Modo de segurança: Criação de pedidos BLOQUEADA via interface web")
        
        # Executar servidor
        app.run(host=host, port=port, debug=debug)
        
    except Exception as e:
        logger.error(f"Erro fatal no servidor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()