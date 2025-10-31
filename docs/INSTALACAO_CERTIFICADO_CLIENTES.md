# 📱 Instalação do Certificado CA nos Dispositivos Clientes

Este guia explica como instalar o certificado CA (rootCA.pem) em dispositivos clientes para que possam acessar o servidor via HTTPS sem avisos de segurança.

## 📋 Pré-requisitos

1. Servidor configurado e rodando com HTTPS
2. Certificado CA disponível (arquivo `rootCA.pem`)
3. Dispositivo cliente na mesma rede que o servidor

## 🎯 Obter o Certificado CA

### No servidor:

```batch
cd backend\ssl
DISTRIBUIR_CERTIFICADO.bat
```

Isso criará a pasta `PARA_CLIENTES` com:
- `rootCA.pem` - O certificado CA
- `INSTRUCOES.md` - Instruções simplificadas

Compartilhe esta pasta com os usuários (rede, pendrive, email, etc.)

---

## 📱 Android

### Método 1: Via Configurações (Recomendado)

1. **Copiar o arquivo**
   - Transfira `rootCA.pem` para o celular (via USB, email, WhatsApp, etc.)
   - Salve em uma pasta conhecida (ex: Downloads)

2. **Abrir Configurações**
   - Vá em **Configurações** → **Segurança** (ou **Segurança e Privacidade**)
   - Em alguns aparelhos: **Configurações** → **Biometria e segurança**

3. **Instalar Certificado**
   - Procure por:
     - **Instalar certificado** ou
     - **Credenciais** → **Instalar da memória** ou
     - **Outras configurações de segurança** → **Instalar do armazenamento**
   
4. **Selecionar Tipo**
   - Escolha **Certificado CA** ou **Certificado de autoridade certificadora**
   - Se perguntar, escolha: **Para VPN e apps**

5. **Localizar Arquivo**
   - Navegue até onde salvou o `rootCA.pem`
   - Selecione o arquivo

6. **Dar um Nome**
   - Digite um nome descritivo, ex: "Gestor Pedidos CA"
   - Toque em **OK**

7. **Confirmar**
   - Pode pedir senha/PIN/biometria
   - Confirme a instalação

8. **Testar**
   - Abra o Chrome ou navegador preferido
   - Acesse: `https://Gestor-pedidos.local:5000`
   - Não deve mais aparecer aviso de segurança!

### Observações Android:

- **Samsung**: Configurações → Biometria e segurança → Outras configurações → Instalar da memória
- **Xiaomi**: Configurações → Senhas e segurança → Privacidade → Criptografia e credenciais → Instalar um certificado
- **Motorola**: Configurações → Segurança → Credenciais → Instalar da memória
- A localização pode variar por fabricante e versão do Android

### Verificar se está instalado:

Configurações → Segurança → Credenciais → Credenciais confiáveis → Aba "Usuário"

---

## 🍎 iOS / iPhone / iPad

### Passo a Passo Completo:

1. **Enviar Certificado para o Dispositivo**
   - **Email**: Envie `rootCA.pem` como anexo para seu email
   - **AirDrop**: Se tiver Mac, use AirDrop
   - **iCloud Drive**: Faça upload e baixe no dispositivo
   - **WhatsApp**: Envie para si mesmo

2. **Abrir o Certificado**
   - Toque no arquivo `rootCA.pem`
   - Uma mensagem aparecerá: "Perfil Baixado"
   - Toque em **Fechar**

3. **Instalar o Perfil**
   - Vá em **Ajustes** (ícone de engrenagem)
   - Role até ver **Perfil Baixado** (ou **Geral** → **VPN e Gerenciamento de Dispositivo**)
   - Toque no perfil "mkcert [nome]"
   - Toque em **Instalar** (canto superior direito)
   - Digite a **senha do iPhone** se solicitado
   - Toque em **Instalar** novamente
   - Toque em **Instalar** mais uma vez (confirmar)
   - Toque em **Concluído**

4. **⚠️ IMPORTANTE: Ativar Confiança no Certificado**
   
   Esta etapa é crucial e muitas vezes esquecida!
   
   - Vá em **Ajustes**
   - **Geral**
   - **Sobre**
   - Role até o final e toque em **Confiança do Certificado** (ou **Certificados Confiáveis**)
   - Na seção "ATIVAR CONFIANÇA TOTAL PARA CERTIFICADOS RAIZ"
   - Encontre "mkcert [nome]"
   - **Ative o interruptor** (deve ficar verde)
   - Confirme "Continuar" no aviso que aparecer

5. **Testar**
   - Abra o Safari
   - Acesse: `https://Gestor-pedidos.local:5000`
   - Não deve aparecer aviso de segurança!
   - O PWA pode ser instalado normalmente

### Verificar se está instalado:

Ajustes → Geral → VPN e Gerenciamento de Dispositivo → Perfis de Configuração

### Remover (se necessário):

Ajustes → Geral → VPN e Gerenciamento de Dispositivo → Selecione o perfil → Remover Perfil

---

## 🪟 Windows (Outros PCs)

### Método 1: Interface Gráfica (Recomendado)

1. **Copiar o Certificado**
   - Transfira `rootCA.pem` para o PC

2. **Abrir o Certificado**
   - Clique **duas vezes** no arquivo `rootCA.pem`
   - Uma janela "Certificado" será aberta

3. **Instalar Certificado**
   - Clique no botão **Instalar Certificado...**
   - Escolha **Máquina Local**
   - Clique em **Avançar**
   - ⚠️ Pode pedir permissões de Administrador - clique em **Sim**

4. **Escolher Repositório**
   - Selecione: **Colocar todos os certificados no repositório a seguir**
   - Clique em **Procurar**
   - Selecione: **Autoridades de Certificação Raiz Confiáveis**
   - Clique em **OK**

5. **Finalizar**
   - Clique em **Avançar**
   - Clique em **Concluir**
   - Um aviso de segurança aparecerá
   - Clique em **Sim**
   - Deve aparecer: "A importação foi bem-sucedida"

6. **Testar**
   - Abra o navegador (Edge, Chrome, etc.)
   - Acesse: `https://Gestor-pedidos.local:5000`
   - Não deve mais aparecer aviso de segurança!

### Método 2: Linha de Comando (Avançado)

```powershell
# Abrir PowerShell como Administrador
certutil -addstore -enterprise -f "Root" rootCA.pem
```

### Verificar se está instalado:

1. Pressione `Win + R`
2. Digite: `certmgr.msc`
3. Vá em: Autoridades de Certificação Raiz Confiáveis → Certificados
4. Procure por "mkcert"

### Remover (se necessário):

1. `Win + R` → `certmgr.msc`
2. Autoridades de Certificação Raiz Confiáveis → Certificados
3. Clique com botão direito em "mkcert" → Excluir

---

## 🐧 Linux

### Ubuntu / Debian:

```bash
# Copiar certificado para pasta do sistema
sudo cp rootCA.pem /usr/local/share/ca-certificates/rootCA.crt

# Atualizar certificados
sudo update-ca-certificates

# Reiniciar navegador
```

### Fedora / CentOS / RHEL:

```bash
# Copiar certificado
sudo cp rootCA.pem /etc/pki/ca-trust/source/anchors/

# Atualizar
sudo update-ca-trust
```

### Arch Linux:

```bash
# Copiar certificado
sudo cp rootCA.pem /etc/ca-certificates/trust-source/anchors/

# Atualizar
sudo trust extract-compat
```

---

## 🍎 macOS

### Interface Gráfica:

1. Abra o arquivo `rootCA.pem`
2. O app "Acesso às Chaves" abrirá
3. Digite a senha do Mac
4. Vá em **Acesso às Chaves** → **Sistema**
5. Encontre o certificado "mkcert"
6. Clique **duas vezes** nele
7. Expanda **Confiar**
8. Em "Ao usar este certificado", escolha: **Confiar Sempre**
9. Feche a janela (digitará senha novamente)

### Linha de Comando:

```bash
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain rootCA.pem
```

---

## 🔍 Solução de Problemas

### ❌ "Certificado não é confiável" / "Sua conexão não é particular"

**Possíveis causas:**

1. **Certificado não foi instalado**
   - Verifique se seguiu todos os passos
   - Em iOS: Certifique-se de ativar a confiança (passo 4)

2. **Certificado instalado no lugar errado**
   - Windows: Deve estar em "Autoridades Raiz Confiáveis", não em "Pessoal"
   - Android: Deve ser "Certificado CA", não "Certificado de usuário"

3. **Navegador não reconhece**
   - Feche e abra o navegador novamente
   - Limpe o cache do navegador
   - Tente outro navegador

4. **Certificado expirado ou inválido**
   - Regenere os certificados no servidor
   - Execute: `backend\ssl\GERAR_CERTIFICADOS_AUTO.bat`
   - Redistribua o novo rootCA.pem

### ❌ "Não consigo acessar o servidor"

**Possíveis causas:**

1. **Dispositivo não está na mesma rede**
   - Conecte-se à mesma rede Wi-Fi do servidor
   - Verifique no servidor: `ipconfig` (Windows) ou `ip addr` (Linux)

2. **Servidor não está rodando**
   - No servidor, execute: `backend\run\abrir_sistema_https.bat`

3. **Firewall bloqueando**
   - Libere a porta 5000 no firewall do servidor
   - Windows: Firewall → Regras de Entrada → Nova Regra → Porta 5000

4. **Hostname não resolve**
   - Teste primeiro via IP: `https://[IP-DO-SERVIDOR]:5000`
   - Se funcionar via IP, o problema é o mDNS

### ❌ "Nome não pode ser resolvido" / "Hostname não encontrado"

**Possíveis causas:**

1. **mDNS não funciona na rede**
   - Redes corporativas podem bloquear mDNS
   - Use o IP do servidor ao invés do hostname

2. **Dispositivo não suporta mDNS**
   - Windows 10/11: Funciona nativamente
   - Android/iOS: Suporta, mas pode depender do roteador
   - Alguns roteadores antigos não propagam mDNS

3. **Solução temporária**
   - Use o IP: `https://192.168.X.XXX:5000`
   - Desvantagem: Se IP mudar, precisa atualizar nos clientes

### ❌ Certificado funciona no PC mas não no celular

**Causa:** Certificados instalados são independentes por dispositivo

**Solução:** Instale o rootCA.pem em CADA dispositivo que vai acessar

---

## 📊 Checklist de Instalação

Use este checklist para cada dispositivo:

### Android:
- [ ] rootCA.pem transferido para o dispositivo
- [ ] Certificado instalado via Configurações → Segurança
- [ ] Escolhido "Certificado CA"
- [ ] Certificado aparece em Credenciais Confiáveis
- [ ] Testado acesso: `https://Gestor-pedidos.local:5000`

### iOS:
- [ ] rootCA.pem enviado para o dispositivo
- [ ] Perfil instalado via Ajustes
- [ ] ⚠️ **CONFIANÇA ATIVADA** em Sobre → Confiança do Certificado
- [ ] Certificado aparece com interruptor verde
- [ ] Testado acesso: `https://Gestor-pedidos.local:5000`

### Windows:
- [ ] rootCA.pem copiado para o PC
- [ ] Certificado instalado em "Autoridades Raiz Confiáveis"
- [ ] Verificado em certmgr.msc
- [ ] Navegador reiniciado
- [ ] Testado acesso: `https://Gestor-pedidos.local:5000`

---

## 🎓 Entendendo o Processo

### Por que instalar o certificado?

O servidor gera um certificado SSL auto-assinado (via mkcert). Por padrão, navegadores não confiam em certificados auto-assinados, mostrando avisos de segurança.

Ao instalar o **rootCA.pem** (Certificado de Autoridade Certificadora), você está dizendo ao dispositivo: "Confie em todos os certificados assinados por esta autoridade".

### É seguro?

**Sim**, para redes locais:
- O certificado funciona **apenas na sua rede local**
- Não afeta a segurança de sites externos
- Pode ser removido a qualquer momento

**Atenção**: Nunca instale certificados CA de fontes desconhecidas!

### Validade

- Certificados mkcert geralmente são válidos por 10 anos
- Se o servidor regenerar certificados, você precisará reinstalar o rootCA.pem

---

## 📚 Recursos Adicionais

- **Documentação mkcert**: https://github.com/FiloSottile/mkcert
- **Configuração HTTPS**: `HTTPS.md`
- **Portabilidade**: `PORTABILIDADE.md`

---

**Última atualização**: Outubro 2025  
**Versão**: 1.0  
**Suporte**: Para dúvidas, consulte a documentação completa do projeto

