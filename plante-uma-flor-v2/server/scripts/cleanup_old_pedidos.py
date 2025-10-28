# -*- coding: utf-8 -*-
"""
Script de limpeza automática de pedidos antigos
"""
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import create_app
from app.models.pedido import Pedido
from app.utils.logger import setup_logger

def cleanup_old_pedidos():
    """Remove pedidos concluídos há mais de 24 horas"""
    
    logger = setup_logger(__name__)
    
    try:
        logger.info("Iniciando limpeza automática de pedidos antigos")
        
        # Criar aplicação
        app = create_app()
        
        with app.app_context():
            # Executar limpeza
            count = Pedido.cleanup_old_pedidos()
            
            if count > 0:
                logger.info(f"Limpeza concluída: {count} pedidos removidos")
                print(f"✅ {count} pedidos antigos removidos com sucesso")
            else:
                logger.info("Nenhum pedido antigo encontrado para remoção")
                print("ℹ️ Nenhum pedido antigo encontrado")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro na limpeza automática: {e}")
        print(f"❌ Erro na limpeza: {e}")
        return False

if __name__ == "__main__":
    print("🧹 Plante Uma Flor v2.0 - Limpeza Automática")
    print("=" * 40)
    
    success = cleanup_old_pedidos()
    
    if success:
        print("✅ Limpeza concluída com sucesso")
        sys.exit(0)
    else:
        print("❌ Erro na limpeza")
        sys.exit(1)