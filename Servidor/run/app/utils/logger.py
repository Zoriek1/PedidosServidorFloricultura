# -*- coding: utf-8 -*-
"""
Sistema de logging
"""
import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logger(name, log_dir='logs'):
    """
    Configura logger para a aplicação
    
    Args:
        name: Nome do logger
        log_dir: Diretório para arquivos de log
        
    Returns:
        logging.Logger: Logger configurado
    """
    # Criar diretório de logs se não existir
    # Se log_dir for relativo, usar relativo ao diretório do servidor
    if not os.path.isabs(log_dir):
        # Obtém o diretório raiz do servidor
        # logger.py está em run/app/utils/, então 4 níveis acima = Servidor/
        base_dir = Path(__file__).parent.parent.parent.parent
        log_path = base_dir / log_dir
    else:
        log_path = Path(log_dir)
    
    log_path.mkdir(exist_ok=True)
    
    # Nome do arquivo de log com data
    log_filename = log_path / f"server_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configurar logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Handler para arquivo
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

