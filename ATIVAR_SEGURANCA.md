# 🔒 Como Ativar Segurança para Acesso Remoto

Guia rápido para proteger seu sistema com autenticação básica.

---

## 🚀 Passo a Passo Rápido

### **1. Configurar Usuário e Senha**

Edite o arquivo `backend/app/middleware.py` e configure seus usuários:

```python
USERS = {
    'admin': 'sua_senha_segura_aqui',
    # Adicione mais usuários se necessário:
    # 'colaborador': 'outra_senha',
}
```

**⚠️ IMPORTANTE:** Use uma senha forte! Exemplo: `MinhaSenh@2024Segura!`

---

### **2. Ativar Middleware de Segurança**

Edite `backend/app/__init__.py` e adicione antes do `return app`:

```python
# No final do arquivo, antes de return app:
from app.middleware import setup_security_middleware

# Ativar segurança (habilite ou desabilite conforme necessário)
ENABLE_AUTH = os.environ.get('ENABLE_AUTH', 'true').lower() == 'true'
ENABLE_RATE_LIMIT = os.environ.get('ENABLE_RATE_LIMIT', 'true').lower() == 'true'

# Configurar middlewares
setup_security_middleware(
    app, 
    enable_auth=ENABLE_AUTH,
    enable_rate_limit=ENABLE_RATE_LIMIT
)
```

---

### **3. Testar Localmente**

```bash
cd backend
python main.py
```

Acesse: `http://localhost:5000`

**Você verá:** Popup de login pedindo usuário e senha

**Digite:**
- Usuário: `admin`
- Senha: `sua_senha_segura_aqui` (a que você configurou)

---

### **4. Desativar Temporariamente (Para Testes)**

Se precisar testar sem autenticação, edite `backend/app/__init__.py`:

```python
# Desativar apenas para desenvolvimento
ENABLE_AUTH = False  # Ou 'false' via variável de ambiente
ENABLE_RATE_LIMIT = False
```

Ou via variável de ambiente:
```bash
set ENABLE_AUTH=false
python main.py
```

---

## 🌐 Para Uso em Produção (Acesso Remoto)

### **Opção 1: Cloudflare Tunnel (Mais Fácil)**

1. **Instalar Cloudflare Tunnel:**
   - Windows: Baixar de https://github.com/cloudflare/cloudflared/releases
   - Extrair `cloudflared.exe` na pasta do projeto

2. **Configurar:**
   ```bash
   # Criar conta gratuita em: https://dash.cloudflare.com
   # Vá em: Zero Trust → Networks → Tunnels
   # Crie um novo tunnel e copie o comando
   ```

3. **Rodar:**
   ```bash
   # No terminal, rode o comando que o Cloudflare forneceu
   # Exemplo:
   cloudflared tunnel --url http://localhost:5000
   ```

4. **Autenticação adicional no Cloudflare:**
   - Zero Trust → Access → Applications
   - Configure login por email (gratuito)

---

### **Opção 2: Servidor com Nginx (Mais Controle)**

Veja o guia completo em: [`ACESSO_REMOTO_SEGURO.md`](ACESSO_REMOTO_SEGURO.md)

**Resumo:**
1. Instalar Nginx no servidor
2. Configurar reverse proxy para `localhost:5000`
3. Obter certificado SSL com Certbot
4. Configurar autenticação HTTP Basic no Nginx (ou usar o middleware)

---

## 📝 Variáveis de Ambiente (Recomendado)

Em produção, use variáveis de ambiente para senhas:

**Windows:**
```powershell
$env:ADMIN_PASSWORD="sua_senha_super_segura"
$env:ENABLE_AUTH="true"
python main.py
```

**Linux/Mac:**
```bash
export ADMIN_PASSWORD="sua_senha_super_segura"
export ENABLE_AUTH="true"
python main.py
```

**No middleware.py:**
```python
USERS = {
    'admin': os.environ.get('ADMIN_PASSWORD', 'senha_padrao_local'),
}
```

---

## ✅ Checklist

- [ ] Senha configurada em `middleware.py`
- [ ] Middleware ativado em `__init__.py`
- [ ] Testado localmente com login
- [ ] Variáveis de ambiente configuradas (produção)
- [ ] HTTPS configurado (se acesso remoto)
- [ ] Firewall configurado (se servidor próprio)

---

## 🆘 Problemas Comuns

### **Não aparece popup de login:**
- Verifique se `ENABLE_AUTH=True` em `__init__.py`
- Limpe cache do navegador (Ctrl+Shift+Del)

### **Esqueci a senha:**
- Edite `middleware.py` e altere a senha
- Reinicie o servidor

### **Quer múltiplos usuários:**
```python
USERS = {
    'admin': 'senha_admin',
    'gerente': 'senha_gerente',
    'operador': 'senha_operador',
}
```

---

## 📞 Próximos Passos

Após ativar a segurança:
1. ✅ Teste localmente
2. ✅ Configure para acesso remoto (Cloudflare Tunnel ou servidor)
3. ✅ Use HTTPS em produção
4. ✅ Configure backups

**Documentação completa:** [`ACESSO_REMOTO_SEGURO.md`](ACESSO_REMOTO_SEGURO.md)


