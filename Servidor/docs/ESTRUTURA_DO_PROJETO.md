# 📁 Estrutura do Projeto - Plante Uma Flor v2.0

## ✅ Estrutura Limpa e Organizada

```
Servidor/
│
├── 🎯 ARQUIVOS PRINCIPAIS
│   ├── main.py                      [Entry point do servidor]
│   ├── config.json                  [Configurações]
│   ├── requirements.txt             [Dependências Python]
│   ├── test_server.py               [Testes automatizados]
│   └── migrate_database.py          [Migration do banco]
│
├── 📂 app/                          [APLICAÇÃO MODULAR]
│   ├── __init__.py                  [Factory Pattern]
│   ├── config.py                    [Configurações da app]
│   │
│   ├── models/                      [Modelos de Dados]
│   │   ├── __init__.py
│   │   └── pedido.py                [Modelo Pedido expandido]
│   │
│   ├── routes/                      [Rotas (Blueprints)]
│   │   ├── __init__.py
│   │   ├── api.py                   [API REST - PDFgen.py]
│   │   └── web.py                   [Interface Web]
│   │
│   └── utils/                       [Utilitários]
│       ├── __init__.py
│       ├── logger.py                [Sistema de logs]
│       └── network_discovery.py     [UDP Broadcast]
│
├── 📂 static/                       [Arquivos Estáticos]
│   ├── database.db                  [Banco de dados SQLite]
│   ├── database_backup_*.db         [Backups automáticos]
│   │
│   ├── css/
│   │   └── style.css                [CSS moderno com gradiente]
│   │
│   └── js/
│       └── app.js                   [JavaScript modular]
│
├── 📂 templates/                    [Templates HTML]
│   ├── base.html                    [Template base]
│   ├── painel.html                  [Painel principal]
│   └── criar_pedido.html            [Formulário]
│
├── 📂 logs/                         [Logs do Servidor]
│   └── server_YYYYMMDD.log          [Logs diários]
│
├── 🚀 SCRIPTS DE INICIALIZAÇÃO
│   ├── INICIAR_AQUI.bat             [Inicialização com testes]
│   ├── iniciar_servidor.bat         [Inicialização simples]
│   ├── Iniciar_Servidor.exe         [Executável]
│   └── Iniciar_Servidor.py          [Script Python]
│
├── 📖 DOCUMENTAÇÃO
│   ├── LEIA-ME_PRIMEIRO.txt         [Resumo executivo]
│   ├── QUICK_START.md               [Início rápido]
│   ├── README_V2.md                 [Manual completo]
│   ├── README.md                    [README original]
│   ├── IMPLEMENTAÇÃO_CONCLUÍDA.md   [Detalhes técnicos]
│   ├── RESUMO_IMPLEMENTAÇÃO_V2.md   [Resumo da implementação]
│   ├── MIGRAÇÃO_CONCLUÍDA.txt       [Guia pós-migration]
│   ├── GUIA_RAPIDO.md               [Guia rápido]
│   ├── INSTRUCOES_INICIO.md         [Instruções de início]
│   └── USO_EXECUTAVEIS.md           [Guia de executáveis]
│
├── 🛠️ BUILD E COMPILAÇÃO
│   ├── Gerador_De_Pedidos.py        [Gerador de pedidos]
│   ├── Gerador_De_Pedidos.exe       [Executável]
│   ├── Gerador_De_Pedidos.spec      [Spec PyInstaller]
│   ├── Iniciar_Servidor.spec        [Spec PyInstaller]
│   └── compilar.bat                 [Script de compilação]
│
└── 📦 _arquivos_antigos_v1/         [ARQUIVOS DA V1.0]
    ├── LEIA-ME.txt                  [Informações]
    ├── app.py                       [Servidor monolítico antigo]
    ├── painel_ifood.html            [Interface estilo iFood]
    ├── style_ifood.css              [CSS estilo iFood]
    ├── style.css                    [CSS antigo]
    ├── script.js                    [JavaScript antigo]
    ├── requirements.txt             [Dependências antigas]
    └── database_backup_*.db         [Backup antigo]
```

## 🎯 Arquivos Importantes para Você

### Para Iniciar o Servidor:
```
INICIAR_AQUI.bat             ← Clique aqui!
```

### Para Desenvolvimento:
```
app/                         ← Código da aplicação
├── models/pedido.py         ← Lógica de pedidos
├── routes/api.py            ← API REST
└── routes/web.py            ← Interface Web
```

### Para Personalização:
```
static/css/style.css         ← Estilos visuais
static/js/app.js             ← Comportamento JS
templates/painel.html        ← Interface principal
config.json                  ← Configurações
```

### Para Documentação:
```
README_V2.md                 ← Manual técnico completo
QUICK_START.md               ← Início rápido (3 passos)
LEIA-ME_PRIMEIRO.txt         ← Comece aqui
```

## 🗑️ Arquivos Limpos

Os seguintes arquivos **já foram movidos** para `_arquivos_antigos_v1/`:
- ✅ `static/app.py` (monolítico) → Substituído por `main.py` + estrutura modular
- ✅ `templates/painel_ifood.html` → Substituído por `painel.html` moderno
- ✅ `templates/style_ifood.css` → Substituído por `static/css/style.css`
- ✅ `static/style_ifood.css` → Substituído por `static/css/style.css`
- ✅ `templates/style.css` → Substituído por `static/css/style.css`
- ✅ `templates/script.js` → Substituído por `static/js/app.js`
- ✅ `static/script.js` → Substituído por `static/js/app.js`
- ✅ `static/requirements.txt` → Duplicado (mantido na raiz)
- ✅ Backups antigos do banco → Mantido apenas o mais recente

## 📊 Estatísticas

- **Total de arquivos**: ~40
- **Linhas de código**: ~3,500
- **Templates HTML**: 3
- **Módulos Python**: 9
- **Arquivos de documentação**: 10
- **Arquivos antigos movidos**: 9

## 💡 Dicas de Navegação

### 1. Estrutura Modular Clara
```
app/
├── models/      → Dados e lógica de negócio
├── routes/      → Endpoints e páginas
└── utils/       → Ferramentas auxiliares
```

### 2. Separação de Responsabilidades
- **Backend**: `app/` (Python)
- **Frontend**: `static/` e `templates/` (HTML/CSS/JS)
- **Configuração**: `config.json`
- **Dados**: `static/database.db`

### 3. Arquivos por Função

**Para Iniciar:**
- `INICIAR_AQUI.bat`
- `main.py`

**Para Testar:**
- `test_server.py`

**Para Configurar:**
- `config.json`

**Para Entender:**
- `README_V2.md`
- `QUICK_START.md`

**Para Migrar:**
- `migrate_database.py`

## 🎨 Fluxo de Requisições

```
Cliente PDFgen.py → POST /api/pedidos → api.py → models/pedido.py → database.db
                                                                           ↓
Navegador → GET / → web.py → templates/painel.html → static/css/style.css
                                                     → static/js/app.js
```

## 🔄 Fluxo de Dados

```
1. Cliente cria pedido (PDFgen.py)
   ↓
2. POST /api/pedidos (routes/api.py)
   ↓
3. Modelo Pedido valida (models/pedido.py)
   ↓
4. Salva no banco (database.db)
   ↓
5. Interface atualiza automaticamente (auto-refresh 30s)
   ↓
6. Usuário visualiza no painel web (templates/painel.html)
```

## 📝 Próximos Passos

Se você quiser:

### Adicionar Nova Funcionalidade
1. Editar: `app/models/pedido.py` (lógica)
2. Editar: `app/routes/api.py` ou `web.py` (endpoints)
3. Editar: `templates/painel.html` (interface)
4. Editar: `static/js/app.js` (comportamento)

### Mudar Visual
1. Editar: `static/css/style.css` (cores, layout)
2. Editar: `templates/painel.html` (estrutura HTML)

### Adicionar Nova Rota
1. Abrir: `app/routes/web.py` ou `api.py`
2. Adicionar: `@web_bp.route('/nova-rota')`
3. Implementar: função da rota

### Gerar Novo Executável
1. Atualizar: `.spec` files (incluir novos arquivos)
2. Executar: `compilar.bat`
3. Testar: em máquina limpa

## 🎯 Conclusão

Projeto **limpo**, **organizado** e **pronto para produção**!

- ✅ Estrutura modular e clara
- ✅ Arquivos antigos preservados (backup)
- ✅ Separação de responsabilidades
- ✅ Documentação completa
- ✅ Fácil de navegar e manter

---

**Para mais informações, consulte**: `README_V2.md` ou `QUICK_START.md`

