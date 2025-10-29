# -*- coding: utf-8 -*-
"""
WSGI entry point para produção
"""
import os
from app import create_app
from app.config import config

# Determinar ambiente
env = os.environ.get('FLASK_ENV', 'production')

# Criar aplicação com configuração de produção
app_config = config.get(env, config['default'])
app = create_app(config={
    'SECRET_KEY': app_config.SECRET_KEY,
    'SQLALCHEMY_DATABASE_URI': app_config.SQLALCHEMY_DATABASE_URI,
    'SQLALCHEMY_TRACK_MODIFICATIONS': app_config.SQLALCHEMY_TRACK_MODIFICATIONS,
    'JSON_AS_ASCII': app_config.JSON_AS_ASCII,
    'JSON_SORT_KEYS': app_config.JSON_SORT_KEYS
})

if __name__ == "__main__":
    app.run()