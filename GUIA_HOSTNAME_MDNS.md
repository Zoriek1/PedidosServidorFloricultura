# 🌐 Guia Rápido: Hostname mDNS

## O que mudou?

Agora o servidor pode ser acessado via **hostname fixo** (ex: `Gestor-pedidos.local`) ao invés de IP!

## ✅ Vantagens

- **Acesso consistente**: Mesmo se o IP mudar, o hostname continua funcionando
- **Fácil de lembrar**: `Gestor-pedidos.local` é mais fácil que `192.168.1.148`
- **Sem reconfiguração**: IP mudou? Não precisa fazer nada!
- **Certificados válidos**: SSL funciona via hostname e todos os IPs

## 🚀 Setup em 3 Passos

### 1️⃣ No Servidor (PC onde o backend roda)

```batch
cd backend
CONFIGURAR_SERVIDOR.bat
```

Este script vai:
- ✅ Instalar mkcert (se necessário)
- ✅ Configurar hostname (padrão: `Gestor-pedidos.local`)
- ✅ Gerar certificados SSL
- ✅ Preparar certificado para distribuição

### 2️⃣ Em Cada Cliente (Outros dispositivos)

**Instalar o certificado CA:**

1. Copie o arquivo: `backend\ssl\PARA_CLIENTES\rootCA.pem`
2. Siga as instruções específicas do seu dispositivo:
   - **Android**: Configurações → Segurança → Instalar certificado CA
   - **iOS**: AirDrop/Email → Ajustes → Perfil → Instalar → **Ativar confiança**
   - **Windows**: Duplo clique → Instalar → Autoridades Raiz Confiáveis

📖 **Guia detalhado**: `docs/INSTALACAO_CERTIFICADO_CLIENTES.md`

### 3️⃣ Acessar o Sistema

**No servidor:**
```
https://localhost:5000
https://Gestor-pedidos.local:5000
```

**Nos clientes (após instalar certificado):**
```
https://Gestor-pedidos.local:5000
```

## 🎯 Exemplo Prático

### Antes (com IP):
- **Servidor**: 192.168.1.148
- **Cliente 1**: Acessa `https://192.168.1.148:5000`
- **Cliente 2**: Acessa `https://192.168.1.148:5000`
- **❌ IP mudou para 192.168.1.200**
  - Precisa atualizar em **todos** os clientes
  - Pode precisar regenerar certificados

### Agora (com hostname):
- **Servidor**: Qualquer IP (ex: 192.168.1.148)
- **Cliente 1**: Acessa `https://Gestor-pedidos.local:5000`
- **Cliente 2**: Acessa `https://Gestor-pedidos.local:5000`
- **✅ IP mudou para 192.168.1.200**
  - **Nada muda!** Hostname continua funcionando
  - Certificado continua válido
  - Clientes não precisam de atualização

## 📱 Instalação do Certificado por Dispositivo

### Android

1. Transfira `rootCA.pem` para o celular
2. **Configurações** → **Segurança**
3. **Instalar certificado** → **Certificado CA**
4. Selecione o arquivo `rootCA.pem`
5. Pronto! Acesse: `https://Gestor-pedidos.local:5000`

### iOS (IMPORTANTE!)

1. Envie `rootCA.pem` por email/AirDrop
2. Abra o arquivo no dispositivo
3. **Ajustes** → **Geral** → **Perfil** → Instalar
4. **⚠️ CRUCIAL**: **Ajustes** → **Geral** → **Sobre** → **Confiança do Certificado**
5. **Ative** o certificado mkcert (deve ficar verde)
6. Pronto! Acesse: `https://Gestor-pedidos.local:5000`

### Windows (outros PCs)

1. Copie `rootCA.pem` para o PC
2. Duplo clique no arquivo
3. **Instalar Certificado** → **Máquina Local**
4. **Autoridades de Certificação Raiz Confiáveis**
5. **Concluir** → Confirmar
6. Pronto! Acesse: `https://Gestor-pedidos.local:5000`

## 🔧 Personalizar Hostname

Edite o arquivo: `backend/config_servidor.ini`

```ini
[SERVIDOR]
hostname = Minha-Loja.local
```

Depois regenere os certificados:

```batch
cd backend\ssl
GERAR_CERTIFICADOS_AUTO.bat
```

## ❓ Perguntas Frequentes

### O hostname funciona fora da rede local?

**Não.** Hostnames `.local` são apenas para rede local (mDNS). Para acesso pela internet, você precisaria de um domínio real.

### Preciso reinstalar o certificado se o hostname mudar?

**Sim.** Se mudar o hostname, precisa:
1. Regenerar certificados no servidor
2. Redistribuir o novo `rootCA.pem`
3. Reinstalar nos clientes

### E se o IP do servidor mudar?

**Não precisa fazer nada!** Essa é a vantagem do hostname. O mDNS resolve automaticamente.

### Funciona em qualquer rede?

**Maioria sim, mas:**
- ✅ Redes domésticas: Funciona
- ✅ Redes pequenas/médias: Funciona
- ⚠️ Redes corporativas: Pode estar bloqueado
- ❌ Internet: Não funciona (apenas rede local)

### E se não funcionar na minha rede?

Use o IP como antes:
```
https://192.168.X.XXX:5000
```

Os certificados continuam válidos para IPs também!

## 📊 Checklist de Instalação

### Servidor:
- [ ] Executado `CONFIGURAR_SERVIDOR.bat`
- [ ] Hostname configurado (ex: `Gestor-pedidos.local`)
- [ ] Certificados gerados
- [ ] Pasta `PARA_CLIENTES` criada
- [ ] Servidor iniciado com HTTPS
- [ ] Testado acesso via hostname no próprio servidor

### Cada Cliente:
- [ ] `rootCA.pem` copiado para o dispositivo
- [ ] Certificado instalado corretamente
- [ ] **iOS**: Confiança ativada (passo crucial!)
- [ ] Testado acesso: `https://Gestor-pedidos.local:5000`
- [ ] Sem avisos de segurança
- [ ] PWA instalado (se desejado)

## 🎉 Pronto!

Agora você tem um sistema HTTPS profissional com acesso via hostname!

**Benefícios conquistados:**
- ✅ Acesso fácil e consistente
- ✅ IP pode mudar livremente
- ✅ Certificados válidos
- ✅ PWA instalável em todos os dispositivos
- ✅ Segurança HTTPS completa

## 📚 Mais Informações

- **Setup detalhado**: `docs/HTTPS.md`
- **Instalação certificado**: `docs/INSTALACAO_CERTIFICADO_CLIENTES.md`
- **Troubleshooting**: `docs/INSTALACAO_CERTIFICADO_CLIENTES.md` (seção de problemas)
- **Portabilidade**: `docs/PORTABILIDADE.md`

---

**Dica Final**: Marque `https://Gestor-pedidos.local:5000` nos favoritos dos dispositivos para acesso rápido!

