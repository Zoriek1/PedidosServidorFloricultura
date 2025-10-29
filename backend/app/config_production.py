# -*- coding: utf-8 -*-
"""
Configurações específicas para produção
"""
import os
from pathlib import Path

class ProductionConfig:
    """Configurações otimizadas para produção"""
    
    # Diretório base do backend
    BASE_DIR = Path(__file__).parent.parent
    
    # Secret key obrigatória em produção
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY deve ser definida em produção!")
    
    # Banco de dados - usar PostgreSQL em produção se disponível
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # PostgreSQL (Railway, Heroku, etc.)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgres://', 'postgresql://')
    else:
        # SQLite como fallback
        DATABASE_PATH = BASE_DIR / 'database.db'
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações gerais
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False
    
    # Servidor
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = False
    
    @staticmethod
    def init_app(app):
        """Inicialização adicional da aplicação"""
        pass