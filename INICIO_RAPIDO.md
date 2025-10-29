# 🚀 Início Rápido - Plante Uma Flor PWA

## Passos para Começar (5 minutos)

### 1. Instalar Dependências

```powershell
cd PWA\backend
pip install -r requirements.txt
```

### 2. Iniciar Servidor

```powershell
python main.py
```

### 3. Acessar no Navegador

**No mesmo computador:**
```
http://localhost:5000
```

**De outro dispositivo (mesma rede WiFi):**
```
http://192.168.1.148:5000
```
*(Substitua pelo IP do seu computador)*

---

## 📱 Instalar como App

### No Desktop (Chrome)

1. Abra http://localhost:5000
2. Clique no ícone ➕ (Instalar) na barra de endereço
3. Clique em "Instalar"
4. Pronto! O app aparecerá no menu Iniciar

### No Celular Android

1. Abra http://IP_DO_SERVIDOR:5000 no Chrome
2. Toque no menu (⋮)
3. Toque em "Adicionar à tela inicial"
4. Toque em "Adicionar"
5. O app aparecerá na tela inicial

### No iPhone/iPad

1. Abra http://IP_DO_SERVIDOR:5000 no Safari
2. Toque no botão Compartilhar (📤)
3. Toque em "Adicionar à Tela de Início"
4. Toque em "Adicionar"
5. O app aparecerá na tela inicial

---

## ✅ Verificar se Está Funcionando

1. **Abra o navegador** em http://localhost:5000
2. **Você deve ver** a tela do painel com:
   - Menu de navegação no topo
   - Estatísticas (Total, Agendados, etc.)
   - Área de pedidos
3. **Clique em "Novo Pedido"** para testar o formulário
4. **Preencha** os campos obrigatórios (marcados com *)
5. **Clique em "Finalizar Pedido"**
6. **Volte ao Painel** para ver o pedido criado

---

## 🔍 Descobrir IP do Computador

### Windows:
```powershell
ipconfig
```
Procure por "Endereço IPv4" (geralmente começa com 192.168)

### Mac/Linux:
```bash
ifconfig
# ou
ip addr show
```

---

## 🐛 Problemas Comuns

### Servidor não inicia
- **Erro de porta ocupada**: Outra aplicação está usando a porta 5000
  - Solução: Feche outras aplicações ou mude a porta em `backend/app/config.py`

### Não consigo acessar de outro dispositivo
- **Firewall bloqueando**: Windows Firewall pode estar bloqueando
  - Solução: Adicione exceção para Python na porta 5000
- **Rede diferente**: Dispositivos precisam estar na mesma rede WiFi
  - Solução: Conecte todos os dispositivos na mesma rede

### Erro ao instalar dependências
- **pip não encontrado**: Python não instalado corretamente
  - Solução: Reinstale Python e marque "Add to PATH"

---

## 📊 Usando o Sistema

### Criar Novo Pedido

1. Clique em "Novo Pedido" no menu
2. Preencha o formulário em 4 etapas:
   - **Etapa 1**: Dados do cliente
   - **Etapa 2**: Produto e data
   - **Etapa 3**: Endereço de entrega
   - **Etapa 4**: Mensagem e pagamento
3. Clique em "Finalizar Pedido"

### Gerenciar Pedidos

1. No Painel, você pode:
   - **Buscar**: Digite nome do cliente ou destinatário
   - **Filtrar**: Clique nos botões de status
   - **Alterar Status**: Use o dropdown em cada pedido
   - **Ver Detalhes**: Clique no ícone do olho (👁️)
   - **Deletar**: Clique no ícone da lixeira (🗑️)

### Modo Offline

O sistema funciona sem internet:
1. Crie pedidos normalmente
2. Eles serão salvos localmente
3. Quando a internet voltar, sincroniza automaticamente

---

## 🎯 Próximos Passos

- ✅ Configure para produção (veja `docs/DEPLOYMENT.md`)
- ✅ Personalize cores em `frontend/assets/css/style.css`
- ✅ Adicione campos personalizados se necessário
- ✅ Configure backup automático do banco de dados

---

## 📚 Documentação Completa

Veja o [README.md](README.md) completo para mais informações.

---

🌺 **Plante Uma Flor** - Sistema de Gestão de Pedidos

