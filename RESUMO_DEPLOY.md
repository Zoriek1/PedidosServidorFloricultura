# 🌺 Plante Uma Flor PWA - Resumo do Deploy

Sua aplicação está pronta para ser hospedada em `app.planteumaflor.com`!

## 🚀 Opções de Hospedagem (Recomendadas)

### 1. **Vercel** ⭐ (Mais Recomendado)
- ✅ **Gratuito** para projetos pessoais
- ✅ **HTTPS automático** (essencial para PWA)
- ✅ **Deploy automático** via Git
- ✅ **CDN global** (carregamento rápido)
- ✅ **Fácil configuração de subdomínio**

**Como fazer:**
1. Push do código para GitHub
2. Conectar conta no [vercel.com](https://vercel.com)
3. Importar repositório
4. Configurar variáveis de ambiente
5. Adicionar domínio `app.planteumaflor.com`

### 2. **Railway** ⭐ (Alternativa Excelente)
- ✅ **Gratuito** com limites generosos
- ✅ **PostgreSQL incluído**
- ✅ **Deploy via Git**
- ✅ **HTTPS automático**

**Como fazer:**
1. Push do código para GitHub
2. Conectar conta no [railway.app](https://railway.app)
3. Criar projeto e importar repositório
4. Configurar variáveis de ambiente
5. Adicionar domínio `app.planteumaflor.com`

## 🔐 Variáveis de Ambiente Necessárias

Configure estas variáveis na plataforma escolhida:

```bash
SECRET_KEY=VzL2Cm!a^tCmXHr$D^J4bA5iHPZ8Pwnr
FLASK_ENV=production
```

**⚠️ IMPORTANTE:** Use a SECRET_KEY gerada acima ou gere uma nova com:
```bash
python3 generate_secret_key.py
```

## 📁 Arquivos Criados para Deploy

- ✅ `vercel.json` - Configuração do Vercel
- ✅ `railway.json` - Configuração do Railway
- ✅ `Procfile` - Configuração do Heroku
- ✅ `requirements.txt` - Dependências Python
- ✅ `backend/wsgi.py` - Entry point para produção
- ✅ `backend/app/config_production.py` - Configurações de produção

## 🌐 Configuração do Subdomínio

### DNS (No seu provedor de domínio):
```
Tipo: CNAME
Nome: app
Valor: [URL fornecida pela plataforma]
TTL: 300
```

### Vercel:
- Valor: `cname.vercel-dns.com`

### Railway:
- Valor: [URL específica fornecida pelo Railway]

## 📱 Teste Final

Após o deploy:

1. **Acesse:** `https://app.planteumaflor.com`
2. **Teste PWA:**
   - Chrome: Ícone de instalação na barra
   - Android: Menu → "Adicionar à tela inicial"
   - iOS: Safari → Compartilhar → "Adicionar à Tela de Início"
3. **Teste funcionalidades:**
   - Criar pedido
   - Visualizar painel
   - Funcionamento offline

## 🎯 Próximos Passos

1. **Escolha uma plataforma** (Vercel ou Railway)
2. **Faça push do código** para GitHub
3. **Configure a plataforma** seguindo o guia
4. **Configure o DNS** no seu provedor
5. **Teste a aplicação** em `https://app.planteumaflor.com`

## 📚 Documentação Completa

- **[DEPLOY.md](DEPLOY.md)** - Guia detalhado de deploy
- **[SUBDOMAIN_SETUP.md](SUBDOMAIN_SETUP.md)** - Configuração do subdomínio
- **[README.md](README.md)** - Documentação da aplicação

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs na plataforma
2. Teste localmente primeiro
3. Verifique as variáveis de ambiente
4. Consulte a documentação específica da plataforma

---

**🎉 Sua aplicação PWA estará online em: `https://app.planteumaflor.com`**

**Tempo estimado para deploy completo: 15-30 minutos**