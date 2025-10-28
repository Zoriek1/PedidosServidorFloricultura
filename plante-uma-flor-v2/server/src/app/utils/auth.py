# -*- coding: utf-8 -*-
"""
Sistema de autenticação para API
"""
import hashlib
import hmac
import time
from functools import wraps
from flask import request, jsonify, current_app
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

def generate_api_key(client_id: str) -> str:
    """Gera chave API para cliente"""
    secret = current_app.config.get('SECRET_KEY', 'default-secret')
    timestamp = str(int(time.time()))
    message = f"{client_id}:{timestamp}"
    
    signature = hmac.new(
        secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return f"{client_id}:{timestamp}:{signature}"

def verify_api_key(api_key: str) -> bool:
    """Verifica chave API"""
    try:
        parts = api_key.split(':')
        if len(parts) != 3:
            return False
        
        client_id, timestamp, signature = parts
        
        # Verificar se timestamp não é muito antigo (1 hora)
        current_time = int(time.time())
        if current_time - int(timestamp) > 3600:
            logger.warning(f"API key expirada para cliente {client_id}")
            return False
        
        # Verificar assinatura
        secret = current_app.config.get('SECRET_KEY', 'default-secret')
        message = f"{client_id}:{timestamp}"
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
        
    except Exception as e:
        logger.error(f"Erro ao verificar API key: {e}")
        return False

def require_api_auth(f):
    """Decorator para requerer autenticação API"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar se autenticação está habilitada
        if not current_app.config.get('API_AUTH_REQUIRED', True):
            return f(*args, **kwargs)
        
        # Verificar header de autorização
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            logger.warning("Tentativa de acesso sem autenticação")
            return jsonify({'error': 'Autenticação necessária'}), 401
        
        # Verificar formato Bearer
        if not auth_header.startswith('Bearer '):
            logger.warning("Formato de autorização inválido")
            return jsonify({'error': 'Formato de autorização inválido'}), 401
        
        # Extrair e verificar API key
        api_key = auth_header[7:]  # Remove 'Bearer '
        if not verify_api_key(api_key):
            logger.warning("API key inválida")
            return jsonify({'error': 'API key inválida ou expirada'}), 401
        
        logger.info("Acesso autorizado via API")
        return f(*args, **kwargs)
    
    return decorated_function

def block_web_creation(f):
    """Decorator para bloquear criação via interface web"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar se bloqueio está habilitado
        if current_app.config.get('WEB_CREATION_BLOCKED', True):
            logger.warning("Tentativa de criação via interface web BLOQUEADA")
            return jsonify({
                'error': 'Criação de pedidos via interface web está desabilitada',
                'message': 'Use apenas o aplicativo desktop para criar pedidos',
                'code': 'WEB_CREATION_BLOCKED'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function