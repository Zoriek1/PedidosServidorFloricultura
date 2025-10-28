# Plante Uma Flor v2.0 - Sistema de Gerenciamento de Pedidos

**Status:** ✅ Validado e Funcional | **Python:** 3.13+ | **Última Atualização:** 28/10/2025

Sistema completo para gerenciamento de pedidos de floricultura com cliente desktop (geração de PDFs) e servidor web (painel de gestão).

---

## 📋 Índice

- [Correções Realizadas](#-correções-realizadas)
- [Validação e Testes](#-validação-e-testes)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação-e-configuração)
- [Build do Cliente](#-build-do-executável)
- [Integração Cliente-Servidor](#-integração-cliente-servidor)
- [Como Usar](#-como-usar)
- [Troubleshooting](#-troubleshooting)

---

## ✅ Correções Realizadas

### 1. Servidor - Erro HTTP 500 (Templates não encontrados)
**Arquivo:** `server/src/app/__init__.py`

**Problema:** Flask não encontrava templates em `painel.html`

**Solução:**
```python
# Configuração explícita de paths
base_dir = Path(__file__).parent.parent
template_dir = base_dir / 'templates'
static_dir = base_dir / 'static'

app = Flask(__name__, 
            template_folder=str(template_dir),
            static_folder=str(static_dir))
```

### 2. Cliente - Import datetime Faltando
**Arquivo:** `client/src/app/gui/main_window.py`

**Problema:** `NameError: name 'datetime' is not defined`

**Solução:** Adicionado `from datetime import datetime` e `import os`

### 3. Cliente - Type Hint Dict Sem Import
**Arquivo:** `client/src/app/core/pdf_generator.py`

**Problema:** Type hint `Dict` usado sem importar

**Solução:** Adicionado `from typing import Dict`

---

## 🧪 Validação e Testes

### Script de Validação

Execute antes de fazer o build:

```bash
python plante-uma-flor-v2/validate_build.py
```

**Validações realizadas:**
- ✅ Estrutura de arquivos do cliente
- ✅ Imports do sistema (tkinter, sqlite3, etc)
- ✅ Imports da aplicação (todos os módulos)
- ✅ Scripts de build disponíveis

### Resultados da Última Validação

```
[OK] Estrutura do Cliente .......... PASSOU
[OK] Imports do Sistema ............ PASSOU
[OK] Imports da Aplicação .......... PASSOU
[OK] Scripts de Build .............. PASSOU

VALIDACAO COMPLETA!
```

---

## 📁 Estrutura do Projeto

```
plante-uma-flor-v2/
├── client/                          # Aplicação Desktop (PDFGen)
│   ├── src/
│   │   ├── main.py                 # Entry point otimizado
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── gui/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── main_window.py  # Janela principal
│   │   │   │   ├── forms/          # Formulários das etapas
│   │   │   │   └── components/     # Componentes reutilizáveis
│   │   │   ├── core/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── pdf_generator.py
│   │   │   │   ├── database.py
│   │   │   │   ├── api_client.py
│   │   │   │   └── validators.py
│   │   │   └── utils/
│   │   │       ├── __init__.py
│   │   │       ├── fonts.py
│   │   │       ├── file_utils.py
│   │   │       └── logger.py
│   │   ├── resources/
│   │   │   ├── fonts/
│   │   │   ├── icons/
│   │   │   └── config.json
│   │   └── build/
│   │       ├── build_exe.py
│   │       └── requirements.txt
│   ├── dist/                       # Executáveis gerados
│   └── logs/                       # Logs da aplicação
├── server/                         # Servidor Web (Gestor)
│   ├── src/
│   │   ├── main.py                 # Entry point do servidor
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   └── pedido.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── api.py
│   │   │   │   └── web.py
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── pedido_service.py
│   │   │   │   └── cleanup_service.py
│   │   │   ├── utils/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── logger.py
│   │   │   │   └── validators.py
│   │   │   └── config.py
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── painel.html
│   │   │   └── components/
│   │   ├── static/
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── images/
│   │   └── requirements.txt
│   ├── database/                   # Banco de dados
│   ├── logs/                       # Logs do servidor
│   └── scripts/
│       ├── start_server.py
│       ├── stop_server.py
│       └── cleanup_old_pedidos.py
├── shared/                         # Código compartilhado
│   ├── __init__.py
│   ├── models/
│   │   └── pedido_schema.py
│   └── utils/
│       ├── __init__.py
│       └── constants.py
├── docs/                          # Documentação
│   ├── api.md
│   ├── deployment.md
│   └── user_guide.md
└── scripts/                       # Scripts de automação
    ├── setup.py
    ├── build_all.py
    └── deploy.py
```

---

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.11+ (testado com 3.13.2)
- pip (gerenciador de pacotes)
- Windows 7+ (para executável)

### Dependências do Servidor

```bash
cd plante-uma-flor-v2/server/src
pip install -r requirements.txt
```

**Principais dependências:**
- Flask >= 2.3.0
- Flask-SQLAlchemy >= 3.0.0
- Flask-CORS >= 4.0.0

### Dependências do Cliente

```bash
cd plante-uma-flor-v2/client/src
pip install -r build/requirements.txt
```

**Principais dependências:**
- reportlab >= 4.0.0 (geração de PDFs)
- requests >= 2.31.0 (comunicação HTTP)
- pyinstaller >= 5.13.0 (build)

---

## 📦 Build do Executável

### Opção 1: Build Completo (Recomendado)

```bash
cd plante-uma-flor-v2/client/src/build
python build_complete.py
```

**Características:**
- ✅ Validação automática de dependências
- ✅ Testes de imports antes do build
- ✅ Inclui config.json no executável
- ✅ Cria scripts auxiliares (.bat)
- ✅ Gera relatório completo do build
- ✅ Executável otimizado (--optimize=2)

**Arquivos gerados:**
```
dist/
├── PlanteUmaFlor-Client.exe    # Executável principal
├── Iniciar_Cliente.bat         # Script de inicialização
├── LEIA-ME.txt                 # Instruções para usuário
├── version.json                # Informações de versão
└── BUILD_REPORT.txt            # Relatório do build
```

### Opção 2: Build Simplificado

```bash
cd plante-uma-flor-v2/client/src/build
python build_simple.py
```

Mais rápido, menos validações.

### Opção 3: Build com Nuitka (Experimental)

```bash
cd plante-uma-flor-v2/client/src/build
python build_exe.py
```

Requer compilador C++ instalado. Gera executável mais otimizado.

---

## 🔄 Integração Cliente-Servidor

### Arquitetura

```
┌─────────────────────────┐
│   CLIENTE DESKTOP       │
│  (PlanteUmaFlor.exe)    │
│                         │
│  • Tkinter GUI          │
│  • Gera PDFs            │
│  • SQLite Local         │
│  • HTTP Client          │
└────────┬────────────────┘
         │
         │ HTTP POST /api/pedidos
         │ (JSON)
         │
┌────────▼────────────────┐
│    SERVIDOR WEB         │
│   (Flask + SQLAlchemy)  │
│                         │
│  • API REST             │
│  • Painel Web           │
│  • SQLite Database      │
│  • Autenticação         │
└─────────────────────────┘
```

### Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/pedidos` | Criar novo pedido |
| GET | `/api/pedidos` | Listar todos os pedidos |
| GET | `/api/pedidos/{id}` | Obter pedido específico |
| PUT | `/api/pedidos/{id}/status` | Atualizar status |
| DELETE | `/api/pedidos/{id}` | Deletar pedido |
| GET | `/api/pedidos/overdue` | Pedidos atrasados |
| POST | `/api/cleanup` | Limpar pedidos antigos |

### Fluxo de Integração

1. **Cliente cria pedido:**
   - Preenche formulário multi-etapas
   - Valida dados obrigatórios
   - Gera PDF localmente (`Documents/Pedidos-Floricultura/`)
   - Salva no banco SQLite local

2. **Cliente envia para servidor:**
   - POST para `/api/pedidos` com dados JSON
   - Se servidor offline: funciona em modo local
   - Se online: sincroniza dados automaticamente

3. **Servidor processa:**
   - Valida autenticação API (Bearer token)
   - Armazena pedido no banco
   - Disponibiliza no painel web

4. **Painel web permite:**
   - Visualizar todos os pedidos
   - Filtrar por status
   - Alterar status do pedido
   - Ver pedidos atrasados
   - Deletar pedidos

---

## 💻 Como Usar

### 1. Iniciar o Servidor

```bash
cd plante-uma-flor-v2/server/src
python main.py
```

**Saída esperada:**
```
INFO - Iniciando Plante Uma Flor v2.0 - Servidor Web
INFO - Banco de dados inicializado
INFO - Servidor iniciando em 0.0.0.0:5000
INFO - Modo de segurança: Criação de pedidos BLOQUEADA via interface web
```

**Acessar painel:** http://localhost:5000

### 2. Executar Cliente (Desenvolvimento)

```bash
cd plante-uma-flor-v2/client/src
python main.py
```

### 3. Executar Cliente (Build)

```bash
cd plante-uma-flor-v2/dist
.\Iniciar_Cliente.bat
```

ou execute diretamente: `PlanteUmaFlor-Client.exe`

### 4. Criar um Pedido

1. Abra o cliente desktop
2. **Etapa 1 - Dados Pessoais:**
   - Cliente (quem envia)
   - Telefone do Cliente **(obrigatório)**
   - Destinatário **(obrigatório)**
   - Tipo: Entrega ou Retirada

3. **Etapa 2 - Dados do Produto:**
   - Nome do Produto
   - Flores e Cor
   - Valor Total
   - Data de Entrega **(obrigatório)**
   - Horário **(obrigatório)**

4. **Etapa 3 - Logística** (se Entrega):
   - Endereço Completo
   - Observações de Entrega

5. **Etapa 4 - Detalhes Finais:**
   - Observações Gerais
   - Mensagem do Cartão
   - Forma de Pagamento

6. Clique em **"Finalizar Pedido"**

**Resultado:**
- ✅ PDF gerado em `Documents/Pedidos-Floricultura/`
- ✅ Salvo no banco local
- ✅ Enviado ao servidor (se online)
- ✅ Visível no painel web

---

## 🔧 Configurações

### Cliente: `client/src/resources/config.json`

```json
{
  "app": {
    "name": "Plante Uma Flor v2.0",
    "version": "2.0.0"
  },
  "server": {
    "base_url": "http://192.168.1.148:5000",
    "timeout": 5,
    "retry_attempts": 3
  },
  "database": {
    "path": "Documents/Pedidos-Floricultura/pedidos.db"
  },
  "pdf": {
    "output_dir": "Documents/Pedidos-Floricultura",
    "font_fallback": "Helvetica"
  }
}
```

### Servidor: `server/src/app/config.py`

```python
class Config:
    SECRET_KEY = 'plante-uma-flor-secret-key-2024-v2'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/pedidos.db'
    
    # Segurança
    SECURITY_ENABLED = True
    API_AUTH_REQUIRED = True
    WEB_CREATION_BLOCKED = True  # Bloquear criação via web
    
    # Limpeza automática
    AUTO_CLEANUP_ENABLED = True
    CLEANUP_AFTER_HOURS = 24  # Limpar pedidos concluídos após 24h
```

### Locais de Arquivos

- **PDFs Gerados:** `C:\Users\[Usuario]\Documents\Pedidos-Floricultura\`
- **Banco Cliente:** `Documents\Pedidos-Floricultura\pedidos.db`
- **Banco Servidor:** `server\database\pedidos.db`
- **Logs Servidor:** `server\logs\server_YYYYMMDD.log`

---

## 🔍 Troubleshooting

### Problema: Servidor dá erro HTTP 500

**Causa:** Templates não encontrados

**Solução:** Já corrigido! Verifique se está usando a versão atualizada do `server/src/app/__init__.py`

### Problema: Cliente não conecta ao servidor

**Verificar:**
1. Servidor está rodando? (`python server/src/main.py`)
2. URL correta no `config.json`?
3. Firewall bloqueando porta 5000?

**Solução temporária:** Cliente funciona em modo offline (salva apenas localmente)

### Problema: Erro ao gerar PDF

**Causa:** ReportLab não instalado

**Solução:**
```bash
pip install reportlab
```

### Problema: Build falha

**Verificar:**
1. Execute primeiro: `python validate_build.py`
2. Instale dependências faltantes
3. Use Python 3.11+

**Dependências de build:**
```bash
pip install pyinstaller reportlab requests
```

### Problema: Import errors no cliente

**Causa:** Imports faltando (já corrigido)

**Verificar:** Execute `validate_build.py` para diagnóstico completo

---

## 📝 Notas de Desenvolvimento

### Tecnologias Utilizadas

**Cliente:**
- Python 3.13+
- Tkinter (GUI nativa)
- ReportLab (geração de PDFs)
- Requests (HTTP client)
- SQLite3 (banco local)
- PyInstaller (build)

**Servidor:**
- Python 3.13+
- Flask 2.3+ (web framework)
- Flask-SQLAlchemy (ORM)
- SQLite (banco de dados)
- Jinja2 (templates)
- JavaScript vanilla (frontend)

### Status do Projeto

- ✅ Código corrigido e validado
- ✅ Todas as validações passando
- ✅ Build testado e funcional
- ✅ Integração cliente-servidor OK
- ✅ PDFs sendo gerados corretamente
- ✅ Painel web funcional
- ✅ Documentação completa

### Próximas Melhorias

- [ ] Autenticação JWT mais robusta
- [ ] Notificações push para novos pedidos
- [ ] Dashboard com estatísticas
- [ ] Exportação para Excel
- [ ] Backup automático do banco
- [ ] Dark mode no painel web
- [ ] App mobile (Flutter/React Native)

---

## 📄 Licença

Propriedade da Plante Uma Flor Floricultura - 2025

---

**Desenvolvido com ❤️ para otimizar o gerenciamento de pedidos**