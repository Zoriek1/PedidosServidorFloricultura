# Plante Uma Flor v2.0 - Sistema de Gerenciamento de Pedidos

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

## 🚀 Instalação e Uso

### Cliente (PDFGen)
```bash
cd client
pip install -r src/build/requirements.txt
python src/main.py
```

### Servidor (Gestor)
```bash
cd server
pip install -r src/requirements.txt
python src/main.py
```

### Build Executável
```bash
cd client
python src/build/build_exe.py
```

## 🔧 Configurações

- **Cliente**: `client/src/resources/config.json`
- **Servidor**: `server/src/app/config.py`
- **Logs**: `client/logs/` e `server/logs/`