# Plante Uma Flor v2.0 - Sistema de Gerenciamento de Pedidos

## ✨ Novidades da Versão 2.0

### 🎨 Interface Moderna
- Design com gradiente roxo profissional
- Cards de estatísticas em tempo real
- Filtros e busca avançados
- Notificações toast
- Modal de confirmação
- Design responsivo para mobile

### 🏗️ Arquitetura Melhorada
- Estrutura modular com Flask Blueprints
- Separação clara: Models, Routes (API/Web), Utils
- Factory Pattern para criação da aplicação
- Sistema de logs estruturado

### 🌐 Descoberta Automática de Rede
- Servidor anuncia presença via UDP broadcast
- Clientes encontram servidor automaticamente
- Solução para IP dinâmico na rede local
- Fallback inteligente para IPs comuns

### 📊 Funcionalidades Novas
- **Alertas de Pedidos Atrasados**: Destaque visual automático
- **Limpeza Automática**: Remove pedidos concluídos antigos
- **Estatísticas Avançadas**: 6 métricas por status
- **Auto-refresh**: Atualização automática a cada 30s
- **Filtros em Tempo Real**: Por status e busca textual

### 🔒 Compatibilidade Total
- API 100% compatível com PDFgen.py existente
- Migração automática do banco de dados
- Preservação de todos os dados existentes
- Campos novos opcionais

## 📁 Estrutura do Projeto

```
Servidor/
├── app/                    # Aplicação principal
│   ├── __init__.py        # Factory pattern
│   ├── config.py          # Configurações
│   ├── models/            # Modelos de dados
│   │   └── pedido.py      # Modelo Pedido expandido
│   ├── routes/            # Rotas (Blueprints)
│   │   ├── api.py         # API REST
│   │   └── web.py         # Interface Web
│   └── utils/             # Utilitários
│       ├── logger.py      # Sistema de logs
│       └── network_discovery.py  # Descoberta de rede
├── static/                # Arquivos estáticos
│   ├── css/
│   │   └── style.css      # CSS moderno
│   ├── js/
│   │   └── app.js         # JavaScript modular
│   └── database.db        # Banco de dados SQLite
├── templates/             # Templates HTML
│   ├── base.html          # Template base
│   ├── painel.html        # Painel principal
│   └── criar_pedido.html  # Formulário
├── logs/                  # Logs do servidor
├── config.json            # Configurações
├── main.py                # Entry point
├── migrate_database.py    # Script de migration
├── test_server.py         # Testes automatizados
└── requirements.txt       # Dependências

```

## 🚀 Instalação e Uso

### 1. Primeira Execução (Migration)

Se você já tem um banco de dados existente:

```bash
python migrate_database.py
```

Isso irá:
- Criar backup automático do banco existente
- Adicionar novas colunas sem perder dados
- Verificar integridade da migration

### 2. Testar o Servidor

```bash
python test_server.py
```

Verifica:
- ✓ Importações
- ✓ Criação da aplicação
- ✓ Banco de dados
- ✓ Rotas (/, /api/stats, /api/pedidos)
- ✓ Network Discovery

### 3. Iniciar o Servidor

**Opção 1 - Script Python:**
```bash
python main.py
```

**Opção 2 - Batch File:**
```bash
iniciar_servidor.bat
```

**Opção 3 - Executável:**
```bash
Iniciar_Servidor.exe
```

O servidor iniciará em:
- **Local**: http://localhost:5000
- **Rede**: http://[SEU_IP]:5000
- **Network Discovery**: Porta UDP 37020

## 🔧 Configuração

### config.json

```json
{
  "server": {
    "host": "0.0.0.0",           // Aceita conexões de qualquer interface
    "port": 5000,                 // Porta do servidor
    "debug": false,               // Modo debug
    "broadcast_enabled": true,    // Habilitar descoberta de rede
    "broadcast_port": 37020,      // Porta UDP para broadcast
    "broadcast_interval": 5       // Intervalo entre broadcasts (segundos)
  },
  "database": {
    "path": "static/database.db"  // Caminho do banco de dados
  }
}
```

## 📡 API REST

### Endpoints

#### Criar Pedido (PDFgen.py compatível)
```http
POST /api/pedidos
Content-Type: application/json

{
  "cliente": "João Silva",
  "produto": "Buquê de Rosas",
  "quantidade": 1,
  "horario": "14:30",
  "dia_entrega": "2024-12-25",
  "destinatario": "Maria Santos",
  "mensagem": "Feliz Aniversário!",
  "telefone_cliente": "(11) 98765-4321",
  "tipo_pedido": "Entrega",
  "endereco": "Rua das Flores, 123",
  "observacoes": "Entregar pela manhã"
}
```

#### Listar Pedidos
```http
GET /api/pedidos?status=agendado&limit=10
```

#### Obter Pedido Específico
```http
GET /api/pedidos/{id}
```

#### Atualizar Status
```http
PUT /api/pedidos/{id}/status
Content-Type: application/json

{"status": "em_producao"}
```

#### Deletar Pedido
```http
DELETE /api/pedidos/{id}
```

#### Estatísticas
```http
GET /api/stats
```

#### Pedidos Atrasados
```http
GET /api/pedidos/overdue
```

#### Limpar Pedidos Antigos
```http
POST /api/cleanup
Content-Type: application/json

{"days": 1}
```

## 🌐 Network Discovery

### Como Funciona

1. **Servidor**: Envia broadcasts UDP a cada 5 segundos com seu IP e porta
2. **Cliente**: Escuta broadcasts e descobre servidor automaticamente
3. **Fallback**: Se broadcast falhar, tenta IPs comuns da rede

### Uso no Cliente (PDFgen.py)

```python
from app.utils.network_discovery import NetworkDiscoveryClient

# Descobrir servidor
client = NetworkDiscoveryClient()
server_url = client.discover_with_fallback()

if server_url:
    print(f"Servidor encontrado: {server_url}")
else:
    print("Servidor não encontrado")
```

## 📊 Status dos Pedidos

- `agendado`: Pedido agendado, aguardando produção
- `em_producao`: Em processo de produção
- `pronto_entrega`: Pronto para entrega
- `em_rota`: Saiu para entrega
- `pronto_retirada`: Pronto para retirada no local
- `concluido`: Pedido finalizado

## 🎨 Interface Web

### Páginas

- **/** - Painel principal com todos os pedidos
- **/criar-pedido** - Formulário de criação manual

### Funcionalidades

1. **Cards de Estatísticas**: Total e por status
2. **Filtros**: Por status e busca textual
3. **Alertas**: Pedidos atrasados destacados
4. **Ações Rápidas**: 
   - Atualizar status (AJAX)
   - Deletar pedido (com confirmação)
   - Limpar pedidos antigos
   - Atualizar painel

## 🔒 Segurança

- Servidor aceita apenas conexões na rede local (0.0.0.0:5000)
- Sem autenticação (sistema interno)
- Aviso de segurança no footer
- Não expor para internet pública

## 🐛 Troubleshooting

### Erro: "no such column"
```bash
python migrate_database.py
```

### Servidor não inicia
```bash
python test_server.py
```

### Cliente não encontra servidor
1. Verificar se firewall permite UDP porta 37020
2. Verificar se estão na mesma rede
3. Testar conexão direta com IP

### Logs
Consultar: `logs/server_YYYYMMDD.log`

## 📝 Changelog

### v2.0 (28/10/2024)
- ✨ Interface moderna com gradiente roxo
- 🏗️ Arquitetura modular (Blueprints)
- 🌐 Sistema de descoberta automática de rede
- 📊 Alertas de pedidos atrasados
- 🧹 Limpeza automática de pedidos antigos
- 📈 Estatísticas avançadas
- 🔍 Filtros e busca em tempo real
- 🎨 Design responsivo
- 🔄 Auto-refresh
- ✅ Testes automatizados
- 📦 Migration automática do BD

## 💻 Requisitos

- Python 3.8+
- Flask 3.0+
- Flask-SQLAlchemy 3.1+
- requests 2.31+

## 🤝 Suporte

Para problemas ou dúvidas:
1. Execute `python test_server.py`
2. Consulte os logs em `logs/`
3. Verifique `config.json`

---

**Plante Uma Flor v2.0** - Sistema completo e moderno de gerenciamento de pedidos para floricultura.

