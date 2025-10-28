# -*- coding: utf-8 -*-
"""
Plante Uma Flor v2.0 - Cliente Desktop
Entry point otimizado com carregamento lazy
"""
import sys
import os
import logging
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent))

# Configurar logging antes de importar outros módulos
from app.utils.logger import setup_logger
logger = setup_logger(__name__)

def main():
    """Entry point principal com inicialização otimizada"""
    try:
        logger.info("Iniciando Plante Uma Flor v2.0 - Cliente Desktop")
        
        # Importação lazy dos módulos pesados
        from app.gui.main_window import MainWindow
        from app.core.database import DatabaseManager
        from app.core.api_client import APIClient
        
        # Inicializar componentes essenciais
        db_manager = DatabaseManager()
        api_client = APIClient()
        
        # Criar e executar aplicação
        app = MainWindow(db_manager, api_client)
        app.run()
        
    except Exception as e:
        logger.error(f"Erro fatal na inicialização: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()