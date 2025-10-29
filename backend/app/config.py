# -*- coding: utf-8 -*-
"""
Configurações da Aplicação Flask
"""
import os
from pathlib import Path

class Config:
    """Configurações base da aplicação"""
    
    # Diretório base do backend
    BASE_DIR = Path(__file__).parent.parent
    
    # Secret key para sessões
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'plante-uma-flor-pwa-secret-key-2024'
    
    # Banco de dados SQLite
    DATABASE_PATH = BASE_DIR / 'database.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações gerais
    JSON_AS_ASCII = False  # Suporte a caracteres UTF-8 em JSON
    JSON_SORT_KEYS = False  # Manter ordem dos campos
    
    # Servidor
    HOST = os.environ.get('HOST') or '0.0.0.0'
    PORT = int(os.environ.get('PORT') or 5000)
    DEBUG = os.environ.get('DEBUG') or False
    
    @staticmethod
    def init_app(app):
        """Inicialização adicional da aplicação"""
        pass

class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True

class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False
    
    # Em produção, usar secret key da variável de ambiente
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this-in-production-please'
    
    @staticmethod
    def init_app(app):
        # Validar SECRET_KEY apenas quando a app for iniciada
        if app.config.get('SECRET_KEY') == 'change-this-in-production-please':
            import warnings
            warnings.warn('SECRET_KEY não definida! Configure a variável de ambiente SECRET_KEY em produção.')

# Dicionário de configurações disponíveis
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

