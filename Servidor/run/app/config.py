# -*- coding: utf-8 -*-
"""
Configurações da aplicação
"""
import os
import json
from pathlib import Path

class Config:
    """Configurações base da aplicação"""
    
    # Segurança
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'plante-uma-flor-secret-key-2024'
    
    # Banco de dados
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Servidor
    HOST = '0.0.0.0'  # Aceita conexões de qualquer interface
    PORT = 5000
    DEBUG = False
    
    # Network Discovery
    BROADCAST_ENABLED = True
    BROADCAST_PORT = 37020
    BROADCAST_INTERVAL = 5  # segundos
    
    @staticmethod
    def load_from_file(config_path='config.json'):
        """Carrega configurações de arquivo JSON se existir"""
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao carregar config.json: {e}")
        return {}
    
    @staticmethod
    def save_to_file(config_dict, config_path='config.json'):
        """Salva configurações em arquivo JSON"""
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar config.json: {e}")
    
    @staticmethod
    def create_default_config():
        """Cria configuração padrão"""
        return {
            "server": {
                "host": "0.0.0.0",
                "port": 5000,
                "debug": False,
                "broadcast_enabled": True,
                "broadcast_port": 37020,
                "broadcast_interval": 5
            },
            "database": {
                "path": "static/database.db"
            }
        }


class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True


class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False


# Configuração padrão
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}

