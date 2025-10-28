# -*- coding: utf-8 -*-
"""
Plante Uma Flor v2.0 - Sistema de Gerenciamento de Pedidos
Factory Pattern com Flask Blueprint
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys
from pathlib import Path

# Instância global do SQLAlchemy
db = SQLAlchemy()

def create_app(config=None):
    """
    Application Factory Pattern
    Cria e configura a aplicação Flask
    """
    # Determinar diretório base
    if getattr(sys, 'frozen', False):
        # Rodando como executável PyInstaller
        base_dir = Path(sys._MEIPASS)
        app_dir = Path(os.path.dirname(sys.executable))
        servidor_dir = app_dir
    else:
        # Rodando como script Python
        # app/__init__.py está em run/app/, então parent.parent.parent = Servidor/
        base_dir = Path(__file__).parent.parent  # run/
        servidor_dir = base_dir.parent  # Servidor/
        app_dir = base_dir
    
    # Criar aplicação Flask
    app = Flask(
        __name__,
        template_folder=str(base_dir / 'templates'),
        static_folder=str(servidor_dir / 'static')
    )
    
    # Configurações
    app.config['SECRET_KEY'] = config.get('secret_key', 'plante-uma-flor-secret-key-2024') if config else 'plante-uma-flor-secret-key-2024'
    
    # Banco de dados
    db_path = servidor_dir / 'static' / 'database.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões
    db.init_app(app)
    
    # Registrar Blueprints
    with app.app_context():
        from app.routes import api_bp, web_bp
        
        app.register_blueprint(api_bp)
        app.register_blueprint(web_bp)
        
        # Criar tabelas
        db.create_all()
    
    return app

