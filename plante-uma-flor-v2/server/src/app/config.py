# -*- coding: utf-8 -*-
"""
Configurações da aplicação
"""
import os
from pathlib import Path

class Config:
    """Configurações base da aplicação"""
    
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'plante-uma-flor-secret-key-2024-v2'
    
    # Banco de dados
    basedir = Path(__file__).parent.parent.parent
    db_path = basedir / "database" / "pedidos.db"
    db_path.parent.mkdir(exist_ok=True)
    
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de segurança
    SECURITY_ENABLED = True
    API_AUTH_REQUIRED = True
    WEB_CREATION_BLOCKED = True  # BLOQUEAR criação via interface web
    
    # Configurações de limpeza automática
    AUTO_CLEANUP_ENABLED = True
    CLEANUP_AFTER_HOURS = 24  # Limpar pedidos concluídos após 24h
    
    # Configurações de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = basedir / "logs" / "server.log"
    LOG_FILE.parent.mkdir(exist_ok=True)
    
    # Configurações de API
    API_TIMEOUT = 30
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Configurações de CORS
    CORS_ORIGINS = ['*']  # Em produção, especificar domínios permitidos