# 🌺 Plante Uma Flor v2.0 - Sistema Completo

## 🎯 O Que É

Sistema completo de gerenciamento de pedidos para floricultura com:
- 🖥️ **Servidor Flask** com painel web moderno
- 💻 **Cliente Desktop** (`PDFgen.exe`) para gerar pedidos
- 🌐 **Descoberta Automática** de rede (IP dinâmico suportado!)
- 📊 **Banco de dados** SQLite sincronizado

## ⚡ Quick Start

### 🖥️ Iniciar Servidor (1 vez, na máquina principal)

```bash
cd Servidor
INICIAR_AQUI.bat
```

Abra navegador: http://localhost:5000

### 💻 Usar Cliente (nas máquinas de atendimento)

```bash
# Executar
PDFgen.exe

# Ou para desenvolvimento
cd Clientes
python PDFgen.py
```

### 🔨 Compilar Cliente (para distribuir)

```bash
cd Clientes
COMPILAR.bat
```

Executável estará em: `dist/PDFgen.exe`

## ✨ Novidades v2.0

### 🌐 Descoberta Automática de Rede
- ❌ **Antes:** IP fixo no código, recompilar a cada mudança
- ✅ **Agora:** Descoberta automática via UDP broadcast
- ✅ **Benefício:** IP pode mudar livremente, zero configuração!

### 🎨 Interface Moderna
- ❌ **Antes:** Design iFood antigo
- ✅ **Agora:** Gradiente roxo/azul profissional
- ✅ **Benefício:** Visual moderno e agradável

### 🏗️ Arquitetura Modular
- ❌ **Antes:** Código monolítico em um arquivo
- ✅ **Agora:** Flask Blueprints, modelos, rotas separadas
- ✅ **Benefício:** Fácil manutenção e expansão

### 📊 Funcionalidades Extras
- ✅ Filtros avançados (status, data, busca)
- ✅ Alertas de pedidos atrasados
- ✅ Limpeza automática (pedidos antigos)
- ✅ Estatísticas em tempo real
- ✅ Campos extras (telefone, tipo, observações)

## 📁 Estrutura do Projeto

```
PedidosServidorFloricultura/
│
├── 📖 README_v2.0.md                          ← Você está aqui
├── 📖 IMPLEMENTAÇÃO_DISCOVERY_COMPLETA.md     ← Detalhes técnicos
├── 📖 COMO_USAR_SISTEMA_COMPLETO.md           ← Guia de uso
│
├── 🖥️ Servidor/                               ← Servidor Flask
│   ├── main.py                               ← Iniciar aqui
│   ├── INICIAR_AQUI.bat                      ← Atalho de início
│   ├── migrate_database.py                   ← Migração de DB
│   ├── test_server.py                        ← Teste completo
│   ├── config.json                           ← Configurações
│   │
│   ├── app/                                  ← Aplicação modular
│   │   ├── __init__.py                       ← Factory pattern
│   │   ├── models/
│   │   │   └── pedido.py                     ← Modelo de dados
│   │   ├── routes/
│   │   │   ├── api.py                        ← API REST
│   │   │   └── web.py                        ← Rotas web
│   │   └── utils/
│   │       ├── logger.py                     ← Logger
│   │       └── network_discovery.py          ← ⭐ Discovery!
│   │
│   ├── static/                               ← Assets
│   │   ├── css/style.css                     ← CSS moderno
│   │   ├── js/app.js                         ← JS modular
│   │   └── database.db                       ← Banco de dados
│   │
│   └── templates/                            ← Templates HTML
│       ├── base.html                         ← Base moderna
│       ├── painel.html                       ← Dashboard
│       └── criar_pedido.html                 ← Formulário
│
└── 💻 Clientes/                               ← Cliente Desktop
    ├── PDFgen.py                             ← ⭐ Com discovery!
    ├── PDFgen.spec                           ← Config PyInstaller
    ├── COMPILAR.bat                          ← ⭐ Compilação auto
    ├── TESTAR_DISCOVERY.py                   ← ⭐ Teste de rede
    ├── README_BUILD.md                       ← Guia de build
    ├── requirements.txt                      ← Dependências
    └── dist/
        └── PDFgen.exe                        ← ⭐ Executável final
```

## 🚀 Fluxo de Trabalho

```
1. Administrador inicia servidor
   └─ cd Servidor
   └─ INICIAR_AQUI.bat
   └─ Servidor anuncia IP via broadcast

2. Usuário 1 abre PDFgen.exe
   └─ Descobre servidor automaticamente
   └─ Preenche formulário
   └─ Gera PDF + envia ao servidor

3. Usuário 2 abre PDFgen.exe
   └─ Descobre servidor automaticamente
   └─ Preenche formulário
   └─ Gera PDF + envia ao servidor

4. Administrador acessa painel web
   └─ http://192.168.X.X:5000
   └─ Vê todos os pedidos
   └─ Gerencia status
   └─ Filtra e pesquisa
```

## 🧪 Testes

### Testar Servidor Completo
```bash
cd Servidor
python test_server.py
```

Verifica:
- ✅ Imports
- ✅ App creation
- ✅ Database
- ✅ Routes
- ✅ Network discovery

### Testar Descoberta de Rede
```bash
cd Clientes
python TESTAR_DISCOVERY.py
```

Verifica:
- ✅ Broadcast UDP funciona
- ✅ Fallback de IPs funciona
- ✅ API responde corretamente

## 🔧 Tecnologias

### Backend
- **Flask 3.1.2** - Framework web
- **SQLAlchemy 2.0** - ORM
- **SQLite** - Banco de dados
- **UDP Broadcast** - Network discovery

### Frontend
- **HTML5 + CSS3** - Interface moderna
- **JavaScript Vanilla** - Interatividade
- **Jinja2** - Templates
- **Gradientes** - Design profissional

### Desktop Client
- **Tkinter** - GUI
- **ReportLab** - Geração de PDF
- **Requests** - HTTP client
- **Socket** - Network discovery
- **PyInstaller** - Build executável

## 📊 Endpoints da API

### Pedidos
- `POST /api/pedidos` - Criar pedido (usado pelo cliente)
- `GET /api/pedidos` - Listar todos
- `GET /api/pedidos/<id>` - Detalhes
- `PUT /api/pedidos/<id>/status` - Atualizar status
- `DELETE /api/pedidos/<id>` - Deletar

### Utilitários
- `GET /api/stats` - Estatísticas
- `GET /api/pedidos/overdue` - Pedidos atrasados
- `POST /api/cleanup` - Limpar pedidos antigos

## 🛡️ Segurança

- ✅ Funciona apenas em rede local (broadcast não sai do roteador)
- ✅ Validação de dados no servidor
- ✅ Tratamento de erros robusto
- ✅ Logs detalhados
- ⚠️ Firewall pode precisar de configuração (portas 5000, 37020)

## 🐛 Troubleshooting Rápido

### "Servidor não encontrado"
1. Servidor está rodando? → `INICIAR_AQUI.bat`
2. Mesma rede? → `ping 192.168.X.X`
3. Firewall? → Permitir portas 5000 (TCP) e 37020 (UDP)
4. Teste: `python TESTAR_DISCOVERY.py`

### "Erro ao gerar PDF"
1. Fontes .ttf na pasta? → Verificar Clientes/
2. Recompilar → `COMPILAR.bat`

### "Painel não abre"
1. Servidor rodando? → Verificar console
2. IP correto? → `ipconfig`
3. Porta ocupada? → Reiniciar servidor

## 📚 Documentação Completa

| Documento | Conteúdo |
|-----------|----------|
| `README_v2.0.md` | Este arquivo - Visão geral |
| `IMPLEMENTAÇÃO_DISCOVERY_COMPLETA.md` | Detalhes técnicos da descoberta de rede |
| `COMO_USAR_SISTEMA_COMPLETO.md` | Guia passo a passo para usuários |
| `Clientes/README_BUILD.md` | Guia de compilação do executável |
| `Servidor/QUICK_START.md` | Início rápido do servidor |
| `Servidor/ESTRUTURA_DO_PROJETO.md` | Arquitetura detalhada |

## ✅ Checklist de Implantação

### Servidor
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Database migrado (`python migrate_database.py`)
- [ ] Testes passando (`python test_server.py`)
- [ ] Servidor iniciando (`INICIAR_AQUI.bat`)
- [ ] Painel acessível no navegador
- [ ] Firewall configurado (se necessário)

### Cliente
- [ ] Dependências instaladas
- [ ] Descoberta testada (`python TESTAR_DISCOVERY.py`)
- [ ] Conecta ao servidor automaticamente
- [ ] Gera PDFs corretamente
- [ ] Envia pedidos ao painel
- [ ] Compilado (`COMPILAR.bat`)
- [ ] Testado em máquina limpa

## 🎉 Resultado Final

### Para Usuários
- ✅ **Zero configuração** - Funciona automaticamente
- ✅ **Interface simples** - Fácil de usar
- ✅ **PDFs profissionais** - Impressos limpos
- ✅ **Sincronização automática** - Com o painel

### Para Administrador
- ✅ **Painel completo** - Gerenciamento visual
- ✅ **Filtros e buscas** - Encontra rápido
- ✅ **Alertas** - Pedidos atrasados em destaque
- ✅ **Estatísticas** - Visão geral do negócio

### Para Desenvolvedor
- ✅ **Código limpo** - Modular e organizado
- ✅ **Documentado** - Guias completos
- ✅ **Testável** - Scripts de teste prontos
- ✅ **Extensível** - Fácil adicionar features

## 🔄 Migração v1.0 → v2.0

Se você já tinha a versão 1.0:

1. ✅ **Backup** - Copie `Servidor/static/database.db`
2. ✅ **Migrar** - Execute `python migrate_database.py`
3. ✅ **Verificar** - Todos os pedidos preservados
4. ✅ **Usar** - Sistema v2.0 pronto!

## 📞 Suporte

### Logs Úteis

**Servidor:**
```
INFO - Servidor de descoberta de rede iniciado
INFO - Enviando broadcast: {...}
INFO - POST /api/pedidos - 201
```

**Cliente:**
```
🔍 Procurando servidor na rede...
✅ Servidor encontrado via broadcast: http://192.168.1.148:5000
📤 Enviando pedido para: http://192.168.1.148:5000/api/pedidos
✅ Pedido #123 enviado ao painel v2.0 com sucesso!
```

## 🎓 Aprendizados e Features

Este projeto demonstra:
- ✅ Flask Blueprint architecture
- ✅ SQLAlchemy ORM
- ✅ UDP Broadcast discovery
- ✅ Modern CSS gradients
- ✅ Vanilla JS modular
- ✅ PyInstaller packaging
- ✅ REST API design
- ✅ Error handling patterns
- ✅ Database migration
- ✅ Logging best practices

## 🌟 Status

**Versão:** 2.0.0  
**Status:** ✅ **COMPLETO E PRONTO PARA PRODUÇÃO**  
**Data:** Outubro 2025

Todas as funcionalidades implementadas, testadas e documentadas.

---

## 🚀 Começar Agora

1. **Servidor:**
   ```bash
   cd Servidor
   INICIAR_AQUI.bat
   ```

2. **Cliente:**
   ```bash
   cd Clientes
   COMPILAR.bat
   dist\PDFgen.exe
   ```

3. **Painel:**
   - Abrir navegador: http://localhost:5000

**Pronto! Sistema funcionando! 🎉**

---

*Desenvolvido com ❤️ para Plante Uma Flor Floricultura*  
*Versão 2.0.0 - Sistema completo de gerenciamento de pedidos*

