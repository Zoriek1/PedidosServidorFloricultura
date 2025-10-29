# Guia de Desenvolvimento

## Estrutura do Projeto

```
PWA/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask factory
│   │   ├── config.py            # Configurações
│   │   ├── models/
│   │   │   └── pedido.py        # Modelo de dados
│   │   └── routes/
│   │       └── api.py           # REST API endpoints
│   ├── ssl/                     # Certificados HTTPS
│   ├── main.py                  # Servidor Flask
│   └── requirements.txt         # Dependências Python
├── frontend/
│   ├── assets/
│   │   ├── css/
│   │   │   └── style.css        # Estilos customizados
│   │   ├── icons/               # Ícones PWA
│   │   └── js/
│   │       ├── app.js           # Aplicação principal
│   │       ├── router.js        # Roteamento SPA
│   │       ├── api.js           # Cliente API
│   │       ├── db.js            # IndexedDB (offline)
│   │       ├── form.js          # Formulário multi-step
│   │       ├── painel.js        # Painel de pedidos
│   │       ├── utils.js         # Utilidades
│   │       ├── masks.js         # Máscaras de input
│   │       ├── validators.js    # Validações
│   │       └── components/      # Componentes reutilizáveis
│   ├── pages/
│   │   ├── criar-pedido.html   # Formulário
│   │   └── painel.html         # Lista de pedidos
│   ├── index.html              # SPA principal
│   ├── manifest.json           # PWA manifest
│   └── sw.js                   # Service Worker
└── docs/                       # Documentação
```

---

## Tecnologias Utilizadas

### Backend

- **Flask** - Framework web Python
- **Flask-CORS** - Suporte a CORS
- **Flask-SQLAlchemy** - ORM
- **SQLite** - Banco de dados
- **Python-dateutil** - Manipulação de datas
- **ReportLab** - Geração de PDFs

### Frontend

- **HTML5** - Estrutura
- **Tailwind CSS** - Estilização (via CDN)
- **JavaScript (ES6+)** - Lógica
- **Service Worker API** - Cache e offline
- **IndexedDB API** - Armazenamento local
- **Fetch API** - Requisições HTTP

---

## Configuração do Ambiente

### Requisitos

- Python 3.8+
- Navegador moderno
- Git

### Instalação

1. Clone o repositório
2. Instale dependências Python:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Configure o banco de dados (criado automaticamente ao iniciar)

4. Inicie o servidor:
   ```bash
   python main.py
   ```

---

## Backend

### Estrutura da API

#### Endpoints Disponíveis

```
GET    /api/health               # Health check
GET    /api/pedidos              # Listar pedidos
POST   /api/pedidos              # Criar pedido
GET    /api/pedidos/:id          # Obter pedido específico
PUT    /api/pedidos/:id          # Atualizar pedido
PUT    /api/pedidos/:id/status   # Atualizar status
DELETE /api/pedidos/:id          # Deletar pedido
GET    /api/stats                # Estatísticas
GET    /api/pedidos/overdue      # Pedidos atrasados
POST   /api/cleanup              # Limpar pedidos antigos
```

### Modelo de Dados

```python
class Pedido:
    id: int
    status: str                  # agendado, producao, pronto, entregue
    tipo: str                    # dia_mae, dia_namorado, aniversario, etc
    
    # Cliente
    remetente: str
    telefone_remetente: str
    destinatario: str
    
    # Produto
    produto: str
    flores: str
    valor: float
    
    # Entrega
    data_entrega: date
    horario_entrega: str
    endereco: str
    cidade: str
    bairro: str
    complemento: str
    
    # Adicionais
    mensagem: str
    forma_pagamento: str
    observacoes: str
    
    # Metadata
    created_at: datetime
    updated_at: datetime
```

### Adicionar Novo Endpoint

1. Edite `backend/app/routes/api.py`
2. Adicione a função com decorador `@bp.route()`
3. Retorne JSON com `jsonify()`

Exemplo:
```python
@bp.route('/custom', methods=['GET'])
def custom_endpoint():
    return jsonify({'message': 'Hello World'})
```

---

## Frontend

### Service Worker

Gerencia cache e funcionalidade offline.

**Arquivo:** `frontend/sw.js`

**Estratégias:**
- **API:** Network First (tenta rede, fallback para cache)
- **Assets:** Cache First (cache primeiro, fallback para rede)

#### Atualizar Cache

Altere o `CACHE_NAME` em `sw.js`:

```javascript
const CACHE_NAME = 'plante-uma-flor-v2';  // Incrementar versão
```

### IndexedDB

Armazena dados offline para sincronização posterior.

**Arquivo:** `frontend/assets/js/db.js`

**Funções principais:**
```javascript
DB.init()                      // Inicializar
DB.savePendingPedido(data)    // Salvar offline
DB.getPendingPedidos()         // Obter pendentes
DB.syncPendingPedidos()        // Sincronizar
```

### Routing

SPA com roteamento client-side.

**Arquivo:** `frontend/assets/js/router.js`

**Adicionar Nova Rota:**
```javascript
const Router = {
    routes: {
        '/': () => Router.navigate('/painel'),
        '/criar-pedido': () => Router.loadPage('criar-pedido'),
        '/painel': () => Router.loadPage('painel'),
        '/nova-pagina': () => Router.loadPage('nova-pagina')  // Nova
    }
};
```

### Componentes

#### Criar Novo Componente

1. Crie arquivo em `frontend/assets/js/components/`
2. Exporte funções
3. Importe em `index.html`

Exemplo `components/meu-componente.js`:
```javascript
const MeuComponente = {
    render(data) {
        return `<div>${data.nome}</div>`;
    }
};
```

---

## Ícones PWA

### Tamanhos Necessários

- 72x72px
- 96x96px
- 128x128px
- 144x144px
- 152x152px
- 192x192px (recomendado)
- 384x384px
- 512x512px

### Gerar Ícones

#### Opção 1: Online (Fácil)

1. Acesse: https://realfavicongenerator.net/
2. Faça upload da imagem base
3. Baixe os ícones gerados
4. Extraia para `frontend/assets/icons/`

#### Opção 2: Script Python

Use o script incluído:

```bash
cd frontend/assets/icons
python gerar_icones.py
```

#### Opção 3: ImageMagick

```bash
# Instale: https://imagemagick.org/

magick icon.svg -resize 72x72 icon-72x72.png
magick icon.svg -resize 96x96 icon-96x96.png
# ... outros tamanhos
```

### Atualizar Manifest

Após gerar ícones, verifique `frontend/manifest.json`:

```json
{
  "icons": [
    {
      "src": "/assets/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

---

## Testes

### Backend

```bash
# Testar API
curl http://localhost:5000/api/health

# Criar pedido
curl -X POST http://localhost:5000/api/pedidos \
  -H "Content-Type: application/json" \
  -d '{"remetente":"Teste",...}'
```

### Frontend

1. Abra DevTools (F12)
2. Aba **Application**:
   - Verifique Service Worker
   - Inspecione Cache Storage
   - Veja IndexedDB
3. Aba **Console**:
   - Veja logs de debug
4. Aba **Network**:
   - Monitore requisições
   - Teste modo offline

### PWA

Use o **Lighthouse** (Chrome DevTools):

1. F12 → Aba **Lighthouse**
2. Selecione "Progressive Web App"
3. Clique "Generate report"
4. Analise pontuação e sugestões

---

## Build e Deploy

### Desenvolvimento

```bash
cd backend
python main.py  # Servidor em http://localhost:5000
```

### Produção

Recomendações:

1. Use WSGI server (Gunicorn, uWSGI)
2. Configure HTTPS
3. Use proxy reverso (Nginx)
4. Configure variáveis de ambiente

Exemplo com Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

---

## Debugging

### Backend

Ative modo debug em `backend/app/config.py`:

```python
DEBUG = True
```

Logs aparecem no terminal.

### Frontend

Console do navegador (F12):

```javascript
console.log('Debug:', data);
console.error('Erro:', error);
```

Habilite logs no Service Worker:
```javascript
// sw.js
console.log('✅ Service Worker: ...');
```

---

## Contribuindo

### Fluxo de Trabalho

1. Clone o repositório
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Faça alterações
4. Teste localmente
5. Commit: `git commit -m "feat: adiciona nova funcionalidade"`
6. Push: `git push origin feature/nova-funcionalidade`
7. Abra Pull Request

### Padrões de Código

**Python:**
- PEP 8
- Docstrings em funções
- Type hints quando possível

**JavaScript:**
- ES6+
- Comentários em funções complexas
- Nomes descritivos de variáveis

### Mensagens de Commit

Siga Conventional Commits:

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `style:` - Formatação
- `refactor:` - Refatoração
- `test:` - Testes
- `chore:` - Manutenção

---

## Performance

### Otimizações Frontend

- Assets são cacheados pelo Service Worker
- CSS inline crítico
- JavaScript carrega no final
- Imagens otimizadas (ícones PNG)

### Otimizações Backend

- SQLite para rapidez em rede local
- Queries otimizadas com índices
- JSON responses minificadas

---

## Recursos Úteis

### Documentação

- [PWA Documentation](https://web.dev/progressive-web-apps/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [IndexedDB API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)

### Ferramentas

- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [Workbox](https://developers.google.com/web/tools/workbox) - Service Worker helpers
- [PWA Builder](https://www.pwabuilder.com/)

---

**Plante Uma Flor** - Sistema de Gestão de Pedidos PWA  
Documentação atualizada: 2024

