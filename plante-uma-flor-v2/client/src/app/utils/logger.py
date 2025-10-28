# -*- coding: utf-8 -*-
"""
Sistema de logging otimizado para o cliente
"""
import logging
import os
from pathlib import Path
from datetime import datetime

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Configura logger otimizado para o cliente"""
    
    # Criar diretório de logs se não existir
    log_dir = Path(__file__).parent.parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Configurar logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Handler para arquivo
    log_file = log_dir / f"client_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Handler para console (apenas erros em produção)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    
    # Formato das mensagens
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger