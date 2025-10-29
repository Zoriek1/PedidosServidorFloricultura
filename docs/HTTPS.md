# Configuração HTTPS para PWA

## Índice

- [Visão Geral](#visão-geral)
- [Início Rápido](#início-rápido)
- [Instalação Detalhada](#instalação-detalhada)
- [Instalar em Outros Dispositivos](#instalar-em-outros-dispositivos)
- [Troubleshooting](#troubleshooting)

---

## Visão Geral

### Por que HTTPS?

**Sem HTTPS:**
- PWA só instala em `localhost` (apenas no servidor)
- Outros dispositivos não podem instalar o PWA
- Navegador mostra "Não seguro"

**Com HTTPS:**
- PWA instalável em TODOS os dispositivos da rede
- Certificado confiável
- Cadeado verde no navegador

### O que é necessário?

- mkcert (gerador de certificados locais)
- Certificados SSL (`cert.pem` e `key.pem`)
- Instalar certificado raiz (`rootCA.pem`) em cada dispositivo

---

## Início Rápido

### 1. Instalar mkcert

```bash
cd backend/ssl
./INSTALAR_MKCERT_SIMPLES.bat
```

ou

```bash
./INSTALAR_MKCERT.bat  # Requer admin
```

### 2. Gerar Certificados

```bash
cd backend/ssl
./GERAR_CERTIFICADOS_AUTO.bat
```

Vai pedir senha de administrador - digite e aguarde!

### 3. Iniciar Servidor HTTPS

```bash
cd backend
./abrir_sistema_https.bat
```

ou

```bash
python main.py --https
```

### 4. Acessar

**No servidor:**
```
https://localhost:5000
```

**Em outros dispositivos:**
```
https://192.168.1.XXX:5000
```

---

## Instalação Detalhada

### Passo 1: Instalar mkcert

#### Opção A: Instalação Simples (Recomendada)

```bash
cd backend/ssl
INSTALAR_MKCERT_SIMPLES.bat
```

Este método baixa o mkcert direto para a pasta do projeto, não requer permissões de administrador.

#### Opção B: Instalação Sistema

```bash
cd backend/ssl
INSTALAR_MKCERT.bat
```

Instala no PATH do sistema. Requer executar como Administrador.

Após a instalação, **feche e abra um novo terminal**.

---

### Passo 2: Gerar Certificados SSL

```bash
cd backend/ssl
GERAR_CERTIFICADOS_AUTO.bat
```

Este script vai:
1. Detectar o mkcert (local ou sistema)
2. Descobrir seu IP automaticamente
3. Pedir senha de administrador (para instalar CA raiz)
4. Gerar `cert.pem` e `key.pem`

Arquivos gerados:
```
backend/ssl/
├── cert.pem    # Certificado público
├── key.pem     # Chave privada
```

---

### Passo 3: Iniciar Servidor HTTPS

#### Opção A: Script completo (abre navegador)
```bash
cd backend
abrir_sistema_https.bat
```

#### Opção B: Apenas servidor
```bash
cd backend
python main.py --https
```

#### Opção C: Background invisível
```bash
cd backend
iniciar_servidor_https_invisivel.vbs
```

---

### Passo 4: Testar

Acesse no navegador:
```
https://localhost:5000
```

Verifique:
- ✅ Cadeado verde aparece
- ✅ Sistema carrega
- ✅ Botão de instalar PWA aparece

---

## Instalar em Outros Dispositivos

Para que outros dispositivos confiem no HTTPS, é necessário instalar o certificado raiz.

### Exportar Certificado Raiz

No servidor, execute:

```bash
mkcert -CAROOT
```

Vai mostrar algo como:
```
C:\Users\SeuNome\AppData\Local\mkcert
```

Abra essa pasta:
```bash
explorer %LOCALAPPDATA%\mkcert
```

Copie o arquivo `rootCA.pem` (NÃO o `rootCA-key.pem`!) para os outros dispositivos.

---

### Windows (Outros PCs)

1. Renomeie `rootCA.pem` para `rootCA.crt`
2. Duplo clique no arquivo
3. Clique em "Instalar Certificado..."
4. Escolha "Computador Local" ou "Usuário Atual"
5. Selecione "Colocar todos os certificados no repositório a seguir"
6. Clique em "Procurar..." e escolha **"Autoridades de Certificação Raiz Confiáveis"**
7. Próximo → Concluir
8. Confirme "Sim" no aviso de segurança

---

### Android

1. Copie `rootCA.pem` para o celular
2. Renomeie para `rootCA.crt`
3. Abra Configurações
4. Navegue até:
   - Segurança → Criptografia e credenciais → Instalar de armazenamento
   - Ou: Biometria e segurança → Outros ajustes → Instalar do armazenamento
5. Selecione o arquivo `rootCA.crt`
6. Digite o PIN/senha se solicitado
7. Defina um nome: "Plante Flor CA"
8. Selecione uso: "VPN e apps"

---

### iOS (iPhone/iPad)

**Importante:** Use apenas o Safari no iOS!

1. Envie `rootCA.pem` por AirDrop ou email
2. Toque no arquivo recebido
3. Aparece "Perfil baixado"
4. Abra Ajustes (Settings)
5. Toque em "Perfil Baixado" (no topo)
6. Toque em "Instalar" (canto superior direito)
7. Digite a senha do iPhone
8. Confirme instalação (mais 2x)
9. **Importante:** Ativar Confiança Total:
   - Ajustes → Geral → Sobre → Ajustes de Confiança do Certificado
   - Ative o switch para o certificado mkcert
   - Confirme "Continuar"

---

### Testar em Outros Dispositivos

Após instalar o certificado:

1. Abra o navegador no dispositivo
2. Acesse: `https://192.168.1.XXX:5000` (substitua pelo IP do servidor)
3. Verifique:
   - ✅ Sem aviso de "não seguro"
   - ✅ Cadeado verde aparece
   - ✅ Sistema carrega

4. Instalar PWA:
   - **Desktop:** Clique no ícone [+] na barra
   - **Mobile:** Menu → "Adicionar à tela inicial"

---

## Troubleshooting

### mkcert não encontrado

**Solução:**
- Feche e abra um novo terminal
- Ou reinicie o computador
- Ou use `INSTALAR_MKCERT_SIMPLES.bat` que não precisa PATH

### Certificados não encontrados

**Solução:**
- Execute `GERAR_CERTIFICADOS_AUTO.bat` primeiro
- Verifique se `cert.pem` e `key.pem` existem em `backend/ssl/`

### ERR_SSL_PROTOCOL_ERROR

**Causas:**
- Servidor não está rodando em HTTPS
- Certificados não foram gerados
- Porta 5000 ocupada

**Solução:**
1. Pare todos os servidores: `parar_servidor.bat`
2. Gere certificados: `GERAR_CERTIFICADOS_AUTO.bat`
3. Inicie HTTPS: `python main.py --https`

### Conexão não segura em outros dispositivos

**Causas:**
- Certificado `rootCA.pem` não instalado
- Certificado instalado no local errado
- iOS: "Confiança Total" não ativada

**Solução:**
- Reinstale o certificado no local correto
- Windows: "Autoridades de Certificação Raiz Confiáveis"
- iOS: Ative "Confiança Total"

### Botão de instalar não aparece

**Solução:**
- Confirme que está em HTTPS (não HTTP)
- Limpe cache: `Ctrl + F5`
- Verifique se ícones do PWA existem
- Feche e abra o navegador

### Múltiplos servidores rodando

Se a porta 5000 está ocupada:

```bash
# Verificar o que está usando
verificar_porta.bat

# Parar tudo
parar_tudo_incluindo_vbs.bat
```

---

## Comandos Úteis

### Descobrir IP local
```bash
ipconfig
# Procure por "IPv4"
```

### Parar servidor
```bash
parar_servidor.bat
```

### Verificar porta 5000
```bash
verificar_porta.bat
```

### Verificar certificados
```bash
cd backend/ssl
dir *.pem
```

---

## Checklist

### No Servidor
- [ ] mkcert instalado
- [ ] Certificados gerados (`cert.pem`, `key.pem`)
- [ ] Servidor em HTTPS iniciado
- [ ] `https://localhost:5000` funciona com cadeado verde
- [ ] PWA instalável localmente
- [ ] `rootCA.pem` exportado

### Em Cada Dispositivo
- [ ] `rootCA.pem` copiado
- [ ] Certificado instalado corretamente
- [ ] iOS: "Confiança Total" ativada
- [ ] `https://IP:5000` acessível
- [ ] Cadeado verde aparece
- [ ] Botão instalar PWA aparece
- [ ] PWA instalado com sucesso

---

## Comparação HTTP vs HTTPS

| Funcionalidade | HTTP | HTTPS |
|----------------|------|-------|
| PWA em localhost | ✅ | ✅ |
| PWA em rede local | ❌ | ✅ |
| Service Worker completo | ⚠️ Limitado | ✅ |
| Cadeado verde | ❌ | ✅ |
| Instalação em dispositivos | ❌ | ✅ |
| Configuração | Simples | Requer certificados |

---

## Dicas de Segurança

- **NUNCA** compartilhe `rootCA-key.pem` (chave privada)
- Compartilhe apenas `rootCA.pem` (certificado público)
- Certificados são válidos apenas na rede local
- Certificados mkcert não expiram por padrão
- IP pode mudar, certificado continua válido

---

## Arquivos do Sistema

```
PWA/
├── backend/
│   ├── ssl/
│   │   ├── INSTALAR_MKCERT_SIMPLES.bat
│   │   ├── INSTALAR_MKCERT.bat
│   │   ├── GERAR_CERTIFICADOS_AUTO.bat
│   │   ├── GERAR_CERTIFICADOS_LOCAL.bat
│   │   ├── GERAR_CERTIFICADOS.bat
│   │   ├── cert.pem (gerado)
│   │   └── key.pem (gerado)
│   ├── iniciar_servidor_https.bat
│   ├── iniciar_servidor_https_invisivel.vbs
│   ├── abrir_sistema_https.bat
│   ├── parar_servidor.bat
│   └── main.py (suporta --https)
└── docs/
    └── HTTPS.md (este arquivo)
```

---

## Resumo Rápido

```bash
# 1. Instalar
cd backend/ssl
INSTALAR_MKCERT_SIMPLES.bat

# 2. Gerar
GERAR_CERTIFICADOS_AUTO.bat

# 3. Iniciar
cd ..
abrir_sistema_https.bat

# 4. Acessar
# https://localhost:5000
```

Para outros dispositivos:
1. Exporte `rootCA.pem`
2. Instale em cada dispositivo
3. Acesse `https://IP:5000`
4. Instale o PWA

---

**Plante Uma Flor** - Sistema de Gestão de Pedidos PWA  
Documentação atualizada: 2024

