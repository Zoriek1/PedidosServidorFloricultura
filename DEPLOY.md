# 🚀 Guia de Deploy - Plante Uma Flor PWA

Este guia mostra como hospedar sua aplicação PWA em um subdomínio do `planteumaflor.com`.

## 🌐 Opções de Hospedagem

### 1. Vercel (Recomendado)

**Vantagens:**
- ✅ Gratuito para projetos pessoais
- ✅ Deploy automático via Git
- ✅ HTTPS automático (essencial para PWA)
- ✅ CDN global
- ✅ Fácil configuração de subdomínio

**Passos:**

1. **Fazer push do código para GitHub:**
   ```bash
   git add .
   git commit -m "Preparar para deploy"
   git push origin main
   ```

2. **Conectar ao Vercel:**
   - Acesse [vercel.com](https://vercel.com)
   - Conecte sua conta GitHub
   - Importe o repositório
   - Configure as variáveis de ambiente:
     - `SECRET_KEY`: Gere uma chave secreta forte
     - `FLASK_ENV`: `production`

3. **Configurar subdomínio:**
   - No painel do Vercel, vá em Settings > Domains
   - Adicione: `app.planteumaflor.com`
   - Configure o DNS no seu provedor de domínio

### 2. Railway

**Vantagens:**
- ✅ Gratuito com limites generosos
- ✅ Banco PostgreSQL incluído
- ✅ Deploy via Git
- ✅ HTTPS automático

**Passos:**

1. **Fazer push do código para GitHub**

2. **Conectar ao Railway:**
   - Acesse [railway.app](https://railway.app)
   - Conecte sua conta GitHub
   - Crie novo projeto
   - Importe o repositório

3. **Configurar variáveis de ambiente:**
   - `SECRET_KEY`: Gere uma chave secreta forte
   - `FLASK_ENV`: `production`

4. **Configurar domínio:**
   - No projeto, vá em Settings > Domains
   - Adicione: `app.planteumaflor.com`

### 3. Heroku (Alternativa)

**Vantagens:**
- ✅ Muito estável
- ✅ Fácil configuração

**Desvantagens:**
- ❌ Pago (não tem mais plano gratuito)

## 🔧 Configuração do DNS

Para configurar o subdomínio `app.planteumaflor.com`:

1. **Acesse o painel do seu provedor de domínio**
2. **Configure o DNS:**
   ```
   Tipo: CNAME
   Nome: app
   Valor: [URL fornecida pela plataforma]
   TTL: 300 (ou padrão)
   ```

## 🔐 Variáveis de Ambiente

Configure estas variáveis na plataforma escolhida:

```bash
SECRET_KEY=sua-chave-secreta-super-forte-aqui
FLASK_ENV=production
```

**Para gerar uma SECRET_KEY segura:**
```python
import secrets
print(secrets.token_hex(32))
```

## 📱 Testando o PWA

Após o deploy:

1. **Acesse:** `https://app.planteumaflor.com`
2. **Teste a instalação:**
   - Chrome: Ícone de instalação na barra de endereços
   - Android: Menu → "Adicionar à tela inicial"
   - iOS: Safari → Compartilhar → "Adicionar à Tela de Início"

## 🔄 Deploy Automático

Com Vercel ou Railway, qualquer push para a branch `main` fará deploy automático.

## 🐛 Troubleshooting

### Erro de CORS
- Verifique se o CORS está configurado corretamente no `app/__init__.py`

### PWA não instala
- Certifique-se de que está usando HTTPS
- Verifique o `manifest.json`

### Banco de dados
- Em produção, considere usar PostgreSQL em vez de SQLite
- Railway oferece PostgreSQL gratuito

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs na plataforma de hospedagem
2. Teste localmente primeiro
3. Verifique as variáveis de ambiente

---

**🎉 Sua aplicação estará online em: `https://app.planteumaflor.com`**