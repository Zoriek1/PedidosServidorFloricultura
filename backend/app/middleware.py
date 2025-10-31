# -*- coding: utf-8 -*-
"""
Middleware de Segurança - Acesso Remoto
Protege o sistema contra acesso não autorizado
"""
from functools import wraps
from flask import request, Response
import os
import hashlib
import time
from datetime import datetime, timedelta

# ============================================
# CONFIGURAÇÃO DE USUÁRIOS
# ============================================
# Edite aqui seus usuários e senhas
# Para maior segurança, use variáveis de ambiente em produção
USERS = {
    'admin': os.environ.get('ADMIN_PASSWORD', 'sua_senha_segura_aqui'),
    # Adicione mais usuários se necessário:
    # 'usuario2': 'outra_senha_segura',
}

# Para maior segurança, você pode usar hash de senhas:
# import bcrypt
# USERS_HASHED = {
#     'admin': '$2b$12$...'  # Hash bcrypt da senha
# }


# ============================================
# AUTENTICAÇÃO BÁSICA HTTP
# ============================================
def check_auth(username, password):
    """
    Verifica se o usuário e senha são válidos
    """
    if username not in USERS:
        return False
    
    expected_password = USERS[username]
    
    # Comparação simples (em produção, use hash)
    return password == expected_password
    
    # Se estiver usando hash bcrypt:
    # import bcrypt
    # if username in USERS_HASHED:
    #     return bcrypt.checkpw(
    #         password.encode('utf-8'),
    #         USERS_HASHED[username].encode('utf-8')
    #     )
    # return False


def requires_auth(f):
    """
    Decorator para proteger rotas com autenticação HTTP Basic
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        
        if not auth or not check_auth(auth.username, auth.password):
            return Response(
                'Acesso negado. Credenciais necessárias.',
                401,
                {
                    'WWW-Authenticate': 'Basic realm="Gestor de Pedidos - Login Necessário"',
                    'Content-Type': 'application/json'
                }
            )
        
        # Armazenar usuário autenticado no request (opcional)
        request.authenticated_user = auth.username
        
        return f(*args, **kwargs)
    
    return decorated


# ============================================
# RATE LIMITING SIMPLES
# ============================================
request_counts = {}

def rate_limit(max_per_minute=60, max_per_hour=1000):
    """
    Rate limiting simples por IP
    Limita requisições para prevenir abuso
    """
    from flask import jsonify
    
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Pegar IP do cliente
            ip = request.remote_addr
            
            # Se vier através de proxy (Nginx), pegar IP real
            if request.headers.get('X-Real-IP'):
                ip = request.headers.get('X-Real-IP')
            elif request.headers.get('X-Forwarded-For'):
                ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
            
            now = time.time()
            
            # Inicializar contador para este IP
            if ip not in request_counts:
                request_counts[ip] = {
                    'minute': [],
                    'hour': []
                }
            
            # Limpar requisições antigas
            request_counts[ip]['minute'] = [
                t for t in request_counts[ip]['minute'] 
                if now - t < 60
            ]
            request_counts[ip]['hour'] = [
                t for t in request_counts[ip]['hour'] 
                if now - t < 3600
            ]
            
            # Verificar limite por minuto
            if len(request_counts[ip]['minute']) >= max_per_minute:
                response = jsonify({
                    'error': 'Rate limit excedido',
                    'message': f'Máximo de {max_per_minute} requisições por minuto',
                    'retry_after': 60
                })
                response.status_code = 429
                response.headers['Retry-After'] = '60'
                return response
            
            # Verificar limite por hora
            if len(request_counts[ip]['hour']) >= max_per_hour:
                response = jsonify({
                    'error': 'Rate limit excedido',
                    'message': f'Máximo de {max_per_hour} requisições por hora',
                    'retry_after': 3600
                })
                response.status_code = 429
                response.headers['Retry-After'] = '3600'
                return response
            
            # Registrar requisição
            request_counts[ip]['minute'].append(now)
            request_counts[ip]['hour'].append(now)
            
            return f(*args, **kwargs)
        
        return decorated
    return decorator


# ============================================
# LOG DE ACESSOS (Básico)
# ============================================
def log_access(ip, endpoint, method, status_code, username=None):
    """
    Registra acesso para auditoria
    Em produção, use um sistema de logging adequado
    """
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f'access_{datetime.now().strftime("%Y-%m-%d")}.log')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = username or 'anonymous'
        f.write(
            f'{timestamp} | {ip} | {user} | {method} {endpoint} | {status_code}\n'
        )


# ============================================
# MIDDLEWARE GLOBAL
# ============================================
def setup_security_middleware(app, enable_auth=True, enable_rate_limit=True):
    """
    Configura middlewares de segurança na aplicação
    """
    from flask import jsonify
    
    @app.before_request
    def before_request():
        """Executado antes de cada requisição"""
        
        # Pular autenticação para health check
        if request.path == '/api/health':
            return None
        
        # Aplicar autenticação se habilitada
        if enable_auth:
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return Response(
                    'Acesso negado. Credenciais necessárias.',
                    401,
                    {
                        'WWW-Authenticate': 'Basic realm="Gestor de Pedidos"',
                        'Content-Type': 'application/json'
                    }
                )
            request.authenticated_user = auth.username
        
        # Rate limiting (exceto health check)
        if enable_rate_limit and request.path != '/api/health':
            ip = request.remote_addr
            if request.headers.get('X-Real-IP'):
                ip = request.headers.get('X-Real-IP')
            elif request.headers.get('X-Forwarded-For'):
                ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
            
            now = time.time()
            if ip not in request_counts:
                request_counts[ip] = {'minute': [], 'hour': []}
            
            request_counts[ip]['minute'] = [
                t for t in request_counts[ip]['minute'] 
                if now - t < 60
            ]
            
            if len(request_counts[ip]['minute']) >= 60:
                return jsonify({
                    'error': 'Rate limit excedido',
                    'message': 'Muitas requisições. Tente novamente em 1 minuto.'
                }), 429
    
    @app.after_request
    def after_request(response):
        """Executado depois de cada requisição"""
        # Log de acesso
        username = getattr(request, 'authenticated_user', None)
        log_access(
            request.remote_addr,
            request.path,
            request.method,
            response.status_code,
            username
        )
        
        return response

