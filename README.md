# Plante Uma Flor - Sistema de Gestão de Pedidos PWA

![Version](https://img.shields.io/badge/version-3.1-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Flask](https://img.shields.io/badge/flask-2.3+-red)
![PWA](https://img.shields.io/badge/PWA-enabled-purple)
![License](https://img.shields.io/badge/license-MIT-yellow)

Progressive Web App moderno para gerenciamento de pedidos de floricultura. Interface web responsiva que funciona em qualquer dispositivo (desktop, tablet, smartphone) com suporte offline completo.

---

## ✨ Principais Características

- **Multiplataforma** - Funciona em Windows, Android, iOS, Linux
- **Offline First** - Funciona sem conexão, sincroniza automaticamente
- **Instalável** - Pode ser instalado como aplicativo nativo
- **Responsivo** - Interface adaptável para todos os tamanhos de tela
- **Rápido** - Carregamento instantâneo com cache inteligente
- **HTTPS** - Suporte a certificados locais para instalação em rede
- **Impressão** - Impressão profissional de pedidos em A4

---

## 🚀 Início Rápido

### Requisitos

- Python 3.8+
- Navegador moderno (Chrome, Edge, Firefox, Safari)
- Rede local (para múltiplos dispositivos)

### Instalação

```bash
# 1. Navegue até o diretório
cd backend

# 2. Instale dependências
pip install -r requirements.txt

# 3. Inicie o servidor
python main.py

# 4. Acesse no navegador
# Local:  http://localhost:5000
# Rede:   http://IP:5000
```

Para instruções detalhadas, veja [`INICIO_RAPIDO.md`](INICIO_RAPIDO.md).

---

## 📖 Documentação

- **[Início Rápido](INICIO_RAPIDO.md)** - Setup e primeiros passos
- **[Instalação PWA](docs/INSTALACAO.md)** - Como instalar em cada dispositivo
- **[Configuração HTTPS](docs/HTTPS.md)** - Setup de certificados SSL
- **[Início Automático](docs/INICIO_AUTOMATICO.md)** - Configurar inicialização do servidor
- **[Desenvolvimento](docs/DESENVOLVIMENTO.md)** - Guia para desenvolvedores

---

## 💻 Funcionalidades

### Criar Pedidos

Formulário intuitivo em 4 etapas:

1. **Dados do Cliente** - Remetente, telefone, destinatário, tipo de pedido
2. **Produto** - Descrição, flores, valor, data e horário de entrega
3. **Endereço** - Endereço completo, cidade, bairro, complemento
4. **Finalização** - Mensagem, forma de pagamento, preview

### Painel de Pedidos

- Listagem com cards coloridos por status
- Filtros por status (Agendado, Produção, Pronto, Entregue, Cancelado)
- Busca em tempo real
- Estatísticas (total, entregues, em produção, atrasados)
- Mudança rápida de status
- **Impressão em A4** com layout profissional

### Funcionalidades Offline

- Cache inteligente de assets
- Armazenamento local com IndexedDB
- Sincronização automática quando online
- Service Worker para funcionamento offline

---

## 🛠️ Tecnologias

### Backend

- Flask 2.3+
- Flask-SQLAlchemy
- Flask-CORS
- SQLite
- Python-dateutil

### Frontend

- HTML5 + CSS3
- JavaScript ES6+
- Tailwind CSS
- Service Worker API
- IndexedDB API
- Fetch API

---

## 📱 Instalação do PWA

### Windows

1. Acesse: `http://localhost:5000` ou `https://IP:5000`
2. Clique no ícone [+] na barra de endereços
3. Clique em "Instalar"

### Android

1. Acesse no Chrome
2. Menu (⋮) → "Adicionar à tela inicial"

### iOS

1. Acesse no Safari
2. Compartilhar (📤) → "Adicionar à Tela de Início"

Para HTTPS em rede local, veja [`docs/HTTPS.md`](docs/HTTPS.md).

---

## 🔒 HTTPS para Rede Local

Para instalar o PWA em outros dispositivos da rede:

```bash
# 1. Instalar mkcert
cd backend/ssl
INSTALAR_MKCERT_SIMPLES.bat

# 2. Gerar certificados
GERAR_CERTIFICADOS_AUTO.bat

# 3. Iniciar servidor HTTPS
cd ..
python main.py --https

# 4. Acessar
# https://localhost:5000
# https://IP:5000
```

Veja documentação completa: [`docs/HTTPS.md`](docs/HTTPS.md)

---

## 📂 Estrutura do Projeto

```
PWA/
├── backend/
│   ├── app/
│   │   ├── models/         # Modelos de dados
│   │   ├── routes/         # REST API endpoints
│   │   ├── __init__.py     # Flask factory
│   │   └── config.py       # Configurações
│   ├── ssl/                # Certificados HTTPS
│   ├── main.py             # Servidor Flask
│   └── requirements.txt    # Dependências Python
├── frontend/
│   ├── assets/
│   │   ├── css/           # Estilos
│   │   ├── icons/         # Ícones PWA
│   │   └── js/            # JavaScript modules
│   ├── pages/             # Páginas SPA
│   ├── index.html         # App principal
│   ├── manifest.json      # PWA manifest
│   └── sw.js              # Service Worker
├── docs/                  # Documentação
├── README.md              # Este arquivo
└── INICIO_RAPIDO.md       # Guia rápido
```

---

## 🎯 REST API

### Endpoints Disponíveis

```
GET    /api/health              # Health check
GET    /api/pedidos             # Listar pedidos
POST   /api/pedidos             # Criar pedido
GET    /api/pedidos/:id         # Obter pedido
PUT    /api/pedidos/:id         # Atualizar pedido
PUT    /api/pedidos/:id/status  # Atualizar status
DELETE /api/pedidos/:id         # Deletar pedido
GET    /api/stats               # Estatísticas
GET    /api/pedidos/overdue     # Pedidos atrasados
POST   /api/cleanup             # Limpar pedidos antigos
```

---

## 📝 Changelog

### v3.1 (Atual)

**Melhorias:**
- ✅ Impressão profissional de pedidos em A4
- ✅ Layout otimizado para logística
- ✅ Destaque visual para informações críticas
- ✅ Suporte completo a HTTPS com mkcert

**Correções:**
- 🐛 Corrigido botão "Finalizar Pedido" no formulário
- 🐛 Melhorada navegação entre steps do formulário
- 🐛 Corrigida sincronização offline

### v3.0

**Inicial:**
- 🎉 Migração completa de Tkinter para PWA
- 🎉 Interface responsiva multiplataforma
- 🎉 Suporte offline com Service Worker
- 🎉 IndexedDB para armazenamento local
- 🎉 REST API completa
- 🎉 Painel com filtros e busca em tempo real

---

## 🔧 Scripts Úteis

### Iniciar Servidor

```bash
# HTTP
python main.py

# HTTPS
python main.py --https

# Background (Windows)
iniciar_servidor_invisivel.vbs
iniciar_servidor_https_invisivel.vbs
```

### Parar Servidor

```bash
parar_servidor.bat
parar_servidor_admin.bat           # Com permissões admin
parar_tudo_incluindo_vbs.bat       # Para tudo
```

### Verificações

```bash
verificar_porta.bat                # Verifica porta 5000
verificar_processos_vbs.bat        # Verifica processos
```

---

## 🚦 Status do Pedido

- **Agendado** (Azul) - Pedido recém-criado
- **Produção** (Amarelo) - Em preparação
- **Pronto** (Verde) - Pronto para entrega
- **Entregue** (Roxo) - Entregue ao destinatário
- **Cancelado** (Vermelho) - Pedido cancelado

---

## 🎨 Temas e Cores

- **Primária:** `#9333ea` (Roxo)
- **Secundária:** `#7c3aed` (Roxo escuro)
- **Accent:** `#a855f7` (Roxo claro)

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m "feat: adiciona nova funcionalidade"`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

Veja [`docs/DESENVOLVIMENTO.md`](docs/DESENVOLVIMENTO.md) para detalhes.

---

## 📄 License

MIT License - veja LICENSE para detalhes.

---

## 💬 Suporte

- Documentação: [`docs/`](docs/)
- Issues: GitHub Issues
- Email: suporte@example.com

---

## 🙏 Agradecimentos

Projeto desenvolvido para modernizar o sistema de gestão de pedidos, substituindo aplicação desktop Tkinter por PWA multiplataforma.

**Tecnologias e Recursos:**
- Flask Framework
- Tailwind CSS
- PWA best practices
- mkcert para HTTPS local

---

**Plante Uma Flor** © 2024 - Sistema de Gestão de Pedidos PWA  
Desenvolvido com ❤️ para floricultura
