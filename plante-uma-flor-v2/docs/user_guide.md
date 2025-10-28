# Plante Uma Flor v2.0 - Guia do Usuário

## 🌺 Visão Geral

O **Plante Uma Flor v2.0** é um sistema completo de gestão de pedidos para floricultura, composto por:

- **Cliente Desktop**: Aplicativo para criação de pedidos (ateliê)
- **Servidor Web**: Painel de gestão e controle (escritório)

## 🖥️ Cliente Desktop (Ateliê)

### Iniciando o Aplicativo

1. **Executável**: Clique duas vezes em `PlanteUmaFlor-Client.exe`
2. **Desenvolvimento**: Execute `python src/main.py`

### Criando um Pedido

O aplicativo guia você através de 4 etapas:

#### **Etapa 1: Dados Pessoais**
- **Cliente**: Nome de quem está enviando
- **Telefone**: Obrigatório para contato
- **Destinatário**: Nome de quem receberá
- **Tipo**: Entrega ou Retirada

#### **Etapa 2: Dados do Produto**
- **Produto**: Descrição do arranjo/buquê
- **Flores e Cor**: Detalhes das flores
- **Valor**: Preço total (formato automático)
- **Data/Hora**: Quando entregar

#### **Etapa 3: Logística (apenas para Entrega)**
- **Endereço**: Local completo da entrega
- **Observações**: Instruções especiais

#### **Etapa 4: Detalhes Finais**
- **Observações Gerais**: Notas sobre o pedido
- **Mensagem do Cartão**: Texto para o cartão
- **Pagamento**: Forma de pagamento

### Recursos do Cliente

- ✅ **Validação Automática**: Campos obrigatórios e formatos
- ✅ **Geração de PDF**: Criação automática do pedido
- ✅ **Sincronização**: Envio automático para o servidor
- ✅ **Backup Local**: Salvamento no banco local
- ✅ **Interface Intuitiva**: Guia passo a passo

## 🌐 Servidor Web (Escritório)

### Acessando o Painel

1. Abra o navegador
2. Acesse: `http://192.168.1.148:5000`
3. Visualize todos os pedidos

### Funcionalidades do Painel

#### **Dashboard Principal**
- 📊 **Estatísticas**: Contadores por status
- ⚠️ **Alertas**: Pedidos atrasados em destaque
- 🔍 **Filtros**: Busca por status ou texto
- 📋 **Lista**: Todos os pedidos organizados

#### **Gerenciamento de Pedidos**

**Status Disponíveis:**
- 🕐 **Agendado**: Pedido criado, aguardando produção
- ⚙️ **Em Produção**: Sendo preparado
- 🚚 **Pronto Entrega**: Pronto para sair
- 🛣️ **Em Rota**: Saindo para entrega
- 📦 **Pronto Retirada**: Aguardando retirada
- ✅ **Concluído**: Finalizado

**Ações Disponíveis:**
- 🔄 **Atualizar Status**: Clique no dropdown
- 🗑️ **Deletar Pedido**: Botão vermelho
- 🧹 **Limpar Antigos**: Remove concluídos há 24h+

#### **Recursos Automáticos**

- ⏰ **Auto-atualização**: A cada 30 segundos
- 🚨 **Alertas de Atraso**: Pedidos atrasados destacados
- 🧹 **Limpeza Automática**: Remove pedidos antigos
- 📱 **Responsivo**: Funciona em celular/tablet

## 🔒 Segurança

### Medidas de Proteção

- 🚫 **Criação via Web BLOQUEADA**: Apenas cliente desktop
- 🔐 **Autenticação API**: Sistema de chaves
- ✅ **Validação Rigorosa**: Todos os dados são validados
- 📝 **Logs Completos**: Todas as ações registradas

### Por que essa Segurança?

- **Previne Erros**: Apenas o aplicativo pode criar pedidos
- **Mantém Integridade**: Dados sempre consistentes
- **Facilita Auditoria**: Logs de todas as operações

## 📱 Fluxo de Trabalho

### No Ateliê (Cliente)

1. **Receber Pedido**: Cliente liga ou chega
2. **Abrir Aplicativo**: Executar cliente desktop
3. **Preencher Dados**: Seguir as 4 etapas
4. **Gerar PDF**: Aplicativo cria automaticamente
5. **Enviar para Servidor**: Sincronização automática
6. **Fechar Aplicativo**: Sistema salva tudo

### No Escritório (Servidor)

1. **Abrir Painel**: Acessar via navegador
2. **Visualizar Pedidos**: Ver todos os pedidos
3. **Atualizar Status**: Conforme progresso
4. **Gerenciar Atrasos**: Atender pedidos atrasados
5. **Limpeza Automática**: Sistema remove antigos

## 🛠️ Solução de Problemas

### Cliente não Conecta

**Sintomas:**
- Aplicativo mostra "Servidor offline"
- PDF é gerado mas não sincroniza

**Soluções:**
1. Verificar se servidor está rodando
2. Verificar IP do servidor
3. Verificar firewall/antivírus
4. Pedido fica salvo localmente

### PDF não é Gerado

**Sintomas:**
- Erro ao gerar PDF
- Arquivo não aparece na pasta

**Soluções:**
1. Verificar permissões da pasta Documents
2. Verificar se há espaço em disco
3. Verificar fontes instaladas
4. Executar como administrador

### Servidor não Inicia

**Sintomas:**
- Erro ao iniciar servidor
- Porta 5000 em uso

**Soluções:**
1. Verificar se Python está instalado
2. Verificar dependências
3. Verificar se porta 5000 está livre
4. Executar `python scripts/setup.py`

## 📊 Relatórios e Exportação

### Exportar Dados

1. **CSV**: Use o botão "Exportar CSV" no cliente
2. **PDFs**: Salvos em `Documents/Pedidos-Floricultura/`
3. **Logs**: Disponíveis em `client/logs/` e `server/logs/`

### Relatórios Disponíveis

- 📈 **Pedidos por Status**: Quantidade em cada fase
- ⏰ **Pedidos Atrasados**: Lista de atrasos
- 📅 **Pedidos por Data**: Organização cronológica
- 💰 **Valores**: Soma dos pedidos (se preenchido)

## 🔄 Backup e Manutenção

### Backup Automático

- **Banco de Dados**: Backup automático diário
- **PDFs**: Salvos permanentemente
- **Logs**: Rotação automática

### Backup Manual

```bash
# Backup do banco
cp server/database/pedidos.db backup_pedidos.db

# Backup dos PDFs
cp -r Documents/Pedidos-Floricultura/ backup_pdfs/
```

## 📞 Suporte Técnico

### Informações do Sistema

- **Versão**: 2.0.0
- **Compatibilidade**: Windows 10/11
- **Python**: 3.7+
- **Navegadores**: Chrome, Firefox, Edge

### Logs de Debug

- **Cliente**: `client/logs/client_YYYYMMDD.log`
- **Servidor**: `server/logs/server_YYYYMMDD.log`

### Comandos Úteis

```bash
# Testar sistema completo
python scripts/test_integration.py

# Configurar sistema
python scripts/setup.py

# Limpar pedidos antigos
python server/scripts/cleanup_old_pedidos.py
```

---

## 🎯 Resumo das Melhorias v2.0

### ✅ **Performance**
- Inicialização 3x mais rápida
- Interface otimizada
- Carregamento lazy de módulos

### ✅ **Segurança**
- Criação via web bloqueada
- Autenticação API
- Validação rigorosa

### ✅ **Usabilidade**
- Interface intuitiva
- Validação em tempo real
- Feedback visual

### ✅ **Automação**
- Limpeza automática
- Alertas de atraso
- Sincronização automática

### ✅ **Manutenibilidade**
- Código modular
- Logs detalhados
- Scripts de automação