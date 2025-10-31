# 🌐 Acessar Sistema Remotamente com Segurança

Guia prático para expor seu **Plante Uma Flor** na internet de forma segura, usando um subdomínio do seu site.

---

## 🎯 O Que Você Precisa

### ✅ **Objetivo:**
- Acessar o sistema de **qualquer lugar** (não só rede local)
- Usar um subdomínio: `gestor.seudominio.com.br`
- **Proteger** contra acesso não autorizado

### ❌ **NÃO precisa:**
- Multi-tenancy (várias lojas)
- Sistema de assinaturas
- Usuários múltiplos com permissões complexas

---

## 🛠️ Opções de Solução

### **Opção 1: Servidor Próprio/VPS (Recomendado)**

#### **Requisitos:**
- Servidor/VPS com IP público (DigitalOcean, Linode, AWS EC2, etc.)
- Domínio próprio (ou subdomínio)
- Acesso SSH ao servidor

#### **Passos:**

**1. Instalar no Servidor:**
```bash
# Instalar Python e dependências
sudo apt update
sudo apt install python3 python3-pip nginx certbot python3-certbot-nginx

# Clonar/copiar seu projeto
cd /var/www
git clone seu-repositorio gestor-pedidos
cd gestor-pedidos/backend
pip3 install -r requirements.txt
```

**2. Configurar Nginx (Reverse Proxy):**
```nginx
# /etc/nginx/sites-available/gestor-pedidos
server {
    listen 80;
    server_name gestor.seudominio.com.br;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/gestor-pedidos /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**3. Obter Certificado SSL (HTTPS):**
```bash
sudo certbot --nginx -d gestor.seudominio.com.br
```

**4. Configurar Firewall:**
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # SSH
sudo ufw enable
```

**5. Rodar como Serviço (PM2 ou systemd):**
```bash
# Com PM2 (recomendado)
npm install -g pm2
cd /var/www/gestor-pedidos/backend
pm2 start main.py --name gestor-pedidos --interpreter python3
pm2 save
pm2 startup  # Para iniciar no boot
```

**6. Adicionar Autenticação Básica (Segurança):**
```bash
# Criar arquivo de senha
sudo apt install apache2-utils
sudo htpasswd -c /etc/nginx/.htpasswd seu_usuario
# Digite a senha quando solicitado

# Editar nginx para adicionar autenticação:
```

```nginx
# Adicionar antes do location /
auth_basic "Acesso Restrito";
auth_basic_user_file /etc/nginx/.htpasswd;
```

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### **Opção 2: Serviços de Túnel (Mais Rápido)**

#### **2.1. Cloudflare Tunnel (Gratuito e Seguro)**

**Vantagens:**
- ✅ Gratuito
- ✅ HTTPS automático
- ✅ Não precisa abrir portas no roteador
- ✅ Proteção DDoS incluída

**Passos:**

1. **Instalar cloudflared:**
```bash
# Windows
# Baixar: https://github.com/cloudflare/cloudflared/releases
# Extrair e colocar na pasta do projeto

# Linux
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
```

2. **Configurar no Cloudflare:**
   - Acesse [Cloudflare Dashboard](https://dash.cloudflare.com)
   - Vá em **Zero Trust** → **Networks** → **Tunnels**
   - Crie um novo tunnel
   - Instale o token no seu servidor

3. **Criar config file:**
```yaml
# config.yml
tunnel: SEU_TUNNEL_ID
credentials-file: /path/to/credentials.json

ingress:
  - hostname: gestor.seudominio.com.br
    service: http://localhost:5000
  - service: http_status:404
```

4. **Rodar:**
```bash
cloudflared tunnel --config config.yml run
```

5. **Adicionar autenticação:**
   - No Cloudflare Zero Trust, configure **Access Policies**
   - Adicione autenticação por email ou SSO

#### **2.2. Ngrok (Mais Simples, Menos Seguro)**

**Atenção:** Versão gratuita tem limitações. Não recomendado para produção.

```bash
# Instalar ngrok
# Baixar: https://ngrok.com/download

# Criar conta e pegar token
ngrok config add-authtoken SEU_TOKEN

# Rodar túnel
ngrok http 5000

# Usar domínio personalizado (precisa plano pago)
ngrok http 5000 --domain=gestor.seudominio.com.br
```

**Desvantagens:**
- ❌ Versão gratuita: URL muda a cada reinício
- ❌ Domínio customizado requer plano pago
- ❌ Sem proteção adicional nativa

---

### **Opção 3: Railway/Render (Deploy Simples)**

**Vantagens:**
- ✅ Deploy automático via Git
- ✅ HTTPS automático
- ✅ Escala automaticamente

**Passos (Railway):**

1. **Criar conta:** [railway.app](https://railway.app)
2. **Criar novo projeto** → **Deploy from GitHub**
3. **Adicionar variáveis de ambiente:**
   ```
   PORT=5000
   FLASK_ENV=production
   SECRET_KEY=seu-secret-key-aqui
   ```
4. **Configurar domínio customizado:**
   - Settings → Domains → Add Custom Domain
   - `gestor.seudominio.com.br`
   - Apontar DNS do seu domínio

5. **Adicionar autenticação:**
   - Railway não tem auth nativo, precisa implementar no código

---

## 🔒 Segurança Básica (Essencial)

### **1. Autenticação Simples (Middleware Flask)**

Adicione autenticação básica no código:

```python
# backend/app/middleware.py
from functools import wraps
from flask import request, Response
import base64

def check_auth(username, password):
    """Verifica usuário e senha"""
    # Configure aqui seus usuários
    users = {
        'admin': 'sua_senha_segura_aqui',
        # Adicione mais usuários se necessário
    }
    return users.get(username) == password

def requires_auth(f):
    """Decorator para proteger rotas"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response(
                'Acesso negado. Credenciais necessárias.',
                401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            )
        return f(*args, **kwargs)
    return decorated
```

**Usar nas rotas:**
```python
# backend/app/routes/api.py
from app.middleware import requires_auth

@api_bp.before_request
@requires_auth
def check_authentication():
    pass  # Todas as rotas protegidas
```

### **2. Rate Limiting Básico**

```python
# backend/app/middleware.py
from flask import request
from functools import wraps
import time

# Simples rate limiting por IP
request_counts = {}

def rate_limit(max_per_minute=60):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            ip = request.remote_addr
            now = time.time()
            
            if ip not in request_counts:
                request_counts[ip] = []
            
            # Limpar requisições antigas (> 1 minuto)
            request_counts[ip] = [t for t in request_counts[ip] if now - t < 60]
            
            if len(request_counts[ip]) >= max_per_minute:
                return {'error': 'Rate limit excedido'}, 429
            
            request_counts[ip].append(now)
            return f(*args, **kwargs)
        return decorated
    return decorator
```

### **3. Configurar Firewall**

**No servidor Linux:**
```bash
# Bloquear todas as portas exceto as necessárias
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### **4. Secret Key Forte**

```python
# backend/app/config.py
import secrets

SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
```

**Variável de ambiente:**
```bash
export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
```

---

## 📝 Configuração DNS

Para usar `gestor.seudominio.com.br`:

1. **No seu provedor de domínio:**
   - Adicione registro **CNAME**:
     - Nome: `gestor`
     - Valor: `seu-servidor.com` (ou IP se A record)

2. **Ou registro A:**
   - Nome: `gestor`
   - Valor: `IP_DO_SERVIDOR`

3. **Aguardar propagação** (pode levar até 48h, geralmente < 1h)

---

## 🚀 Script de Inicialização Segura

Crie um script para iniciar com segurança:

```python
# backend/main_production.py
import os
from app import create_app
from app.config import ProductionConfig

if __name__ == '__main__':
    app = create_app(config={
        'SECRET_KEY': os.environ.get('SECRET_KEY', 'CHANGE_THIS_IN_PRODUCTION'),
        'SQLALCHEMY_DATABASE_URI': ProductionConfig.SQLALCHEMY_DATABASE_URI,
        'DEBUG': False,
        'HOST': '127.0.0.1',  # Só aceita conexões locais (Nginx faz proxy)
        'PORT': 5000
    })
    
    # Usar gunicorn ou waitress em produção
    from waitress import serve
    serve(app, host='127.0.0.1', port=5000)
```

**Atualizar requirements.txt:**
```
waitress==2.1.2  # Servidor WSGI para produção
```

---

## ✅ Checklist de Segurança

- [ ] HTTPS configurado (certificado válido)
- [ ] Autenticação básica ativada
- [ ] Firewall configurado
- [ ] SECRET_KEY forte e em variável de ambiente
- [ ] DEBUG=False em produção
- [ ] Rate limiting ativado
- [ ] Backups automáticos configurados
- [ ] Logs de acesso monitorados
- [ ] Atualizações de segurança aplicadas

---

## 🎯 Recomendação Final

**Para seu caso (acesso remoto simples e seguro):**

1. **Se tem servidor/VPS:** Opção 1 (Nginx + Certbot + Auth básica)
2. **Se não tem servidor:** Opção 2.1 (Cloudflare Tunnel) - **mais fácil**
3. **Se quer deploy automático:** Opção 3 (Railway/Render)

**Cloudflare Tunnel é ideal se:**
- ✅ Não quer configurar servidor
- ✅ Quer HTTPS automático
- ✅ Quer proteção DDoS
- ✅ Quer autenticação fácil via email

---

## 📞 Próximos Passos

Qual opção você prefere? Posso ajudar a implementar qualquer uma delas!

**Mais simples:** Cloudflare Tunnel  
**Mais controle:** Servidor próprio + Nginx  
**Mais automático:** Railway/Render


