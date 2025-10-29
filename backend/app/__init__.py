# -*- coding: utf-8 -*-
"""
Plante Uma Flor v3.0 - PWA
Sistema de Gerenciamento de Pedidos - Backend Flask API
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from pathlib import Path

# Instância global do SQLAlchemy
db = SQLAlchemy()

def create_app(config=None):
    """
    Application Factory Pattern
    Cria e configura a aplicação Flask com CORS para PWA
    """
    # Criar aplicação Flask
    app = Flask(__name__)
    
    # Habilitar CORS para permitir requisições do frontend PWA
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Carregar configurações
    if config:
        app.config.update(config)
    else:
        from app.config import Config
        app.config.from_object(Config)
    
    # Inicializar extensões
    db.init_app(app)
    
    # Registrar Blueprints (apenas API REST)
    with app.app_context():
        from app.routes.api import api_bp
        
        app.register_blueprint(api_bp)
        
        # Criar tabelas automaticamente
        db.create_all()
        
        print("✅ Banco de dados inicializado")
        print(f"✅ Tabelas criadas: {db.metadata.tables.keys()}")
    
    # Servir arquivos estáticos do frontend PWA
    @app.route('/')
    @app.route('/<path:path>')
    def serve_frontend(path='index.html'):
        """Serve arquivos do frontend PWA"""
        from flask import send_from_directory
        frontend_dir = Path(__file__).parent.parent.parent / 'frontend'
        
        # Se o arquivo existe, serve ele
        file_path = frontend_dir / path
        if file_path.exists() and file_path.is_file():
            return send_from_directory(str(frontend_dir), path)
        
        # Caso contrário, serve o index.html (SPA routing)
        return send_from_directory(str(frontend_dir), 'index.html')
    
    return app

