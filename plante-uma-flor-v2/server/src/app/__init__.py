# -*- coding: utf-8 -*-
"""
Plante Uma Flor v2.0 - Servidor Web
Factory de aplicação Flask
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.utils.logger import setup_logger

# Inicializar extensões
db = SQLAlchemy()

def create_app():
    """Factory de aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações
    app.config.from_object(Config)
    
    # Inicializar extensões
    db.init_app(app)
    
    # Configurar logging
    logger = setup_logger(__name__)
    
    # Registrar blueprints
    from app.routes.web import web_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Criar tabelas do banco
    with app.app_context():
        db.create_all()
        logger.info("Banco de dados inicializado")
    
    return app