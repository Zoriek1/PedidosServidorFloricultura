# 🌐 Configuração de Subdomínio - app.planteumaflor.com

Este guia mostra como configurar o subdomínio `app.planteumaflor.com` para sua aplicação PWA.

## 📋 Pré-requisitos

- ✅ Domínio `planteumaflor.com` configurado
- ✅ Acesso ao painel de DNS do provedor do domínio
- ✅ Aplicação deployada em uma das plataformas

## 🔧 Configuração do DNS

### 1. Vercel (Recomendado)

**Passos:**

1. **No Vercel:**
   - Acesse seu projeto
   - Vá em Settings > Domains
   - Clique em "Add Domain"
   - Digite: `app.planteumaflor.com`
   - Clique em "Add"

2. **No seu provedor de DNS:**
   ```
   Tipo: CNAME
   Nome: app
   Valor: cname.vercel-dns.com
   TTL: 300 (ou padrão)
   ```

### 2. Railway

**Passos:**

1. **No Railway:**
   - Acesse seu projeto
   - Vá em Settings > Domains
   - Clique em "Custom Domain"
   - Digite: `app.planteumaflor.com`
   - Copie a URL fornecida

2. **No seu provedor de DNS:**
   ```
   Tipo: CNAME
   Nome: app
   Valor: [URL fornecida pelo Railway]
   TTL: 300 (ou padrão)
   ```

### 3. Heroku

**Passos:**

1. **No Heroku:**
   - Acesse seu app
   - Vá em Settings > Domains
   - Clique em "Add Domain"
   - Digite: `app.planteumaflor.com`

2. **No seu provedor de DNS:**
   ```
   Tipo: CNAME
   Nome: app
   Valor: [nome-do-app].herokuapp.com
   TTL: 300 (ou padrão)
   ```

## ⏱️ Tempo de Propagação

- **Propagação DNS:** 5-60 minutos
- **Verificação:** Use `nslookup app.planteumaflor.com`

## 🔍 Verificação

### 1. Teste DNS
```bash
nslookup app.planteumaflor.com
```

### 2. Teste HTTPS
- Acesse: `https://app.planteumaflor.com`
- Verifique se carrega sem erros de certificado

### 3. Teste PWA
- Abra no Chrome
- Verifique se aparece o ícone de instalação
- Teste a instalação

## 🐛 Troubleshooting

### DNS não resolve
- Aguarde até 1 hora para propagação
- Verifique se o CNAME está correto
- Teste com `dig app.planteumaflor.com`

### Certificado SSL inválido
- Aguarde até 24 horas para o certificado ser emitido
- Verifique se o domínio está configurado corretamente

### PWA não instala
- Certifique-se de que está usando HTTPS
- Verifique o console do navegador para erros
- Teste o `manifest.json`

## 📱 Teste Final

Após a configuração:

1. **Acesse:** `https://app.planteumaflor.com`
2. **Teste todas as funcionalidades:**
   - Criar pedido
   - Visualizar painel
   - Instalar PWA
   - Funcionamento offline

## 🎉 Sucesso!

Sua aplicação estará disponível em:
**https://app.planteumaflor.com**

---

**💡 Dica:** Mantenha um backup da configuração DNS caso precise restaurar.