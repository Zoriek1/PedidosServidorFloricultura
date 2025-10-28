# Sistema de Gerenciamento de Pedidos - Plante Uma Flor

Sistema completo para gerenciamento de pedidos de floricultura com geração de PDFs e painel web.

## 📁 Estrutura do Projeto

```
/workspace/
├── Clientes/                 # Aplicação Desktop (Gerador de PDFs)
│   ├── PDFgen.py            # Aplicação principal
│   ├── PDFgen.spec          # Configuração de compilação
│   ├── requirements.txt     # Dependências Python
│   ├── fonts/               # Fontes para PDFs
│   └── README.md            # Documentação do cliente
├── Servidor/                # Servidor Web Flask
│   ├── app.py              # Servidor Flask principal
│   ├── database.db         # Banco de dados SQLite
│   ├── requirements.txt    # Dependências Python
│   ├── static/             # Arquivos estáticos (CSS, JS)
│   ├── templates/          # Templates HTML
│   ├── Iniciar_Servidor.py # Script de inicialização
│   ├── Iniciar_Servidor.spec # Configuração de compilação
│   └── README.md           # Documentação do servidor
└── README.md               # Este arquivo
```

## 🚀 Como Usar

### Opção 1: Executar diretamente (Desenvolvimento)

1. **Iniciar o Servidor:**
   ```bash
   cd Servidor
   pip install -r requirements.txt
   python app.py
   ```

2. **Executar o Cliente:**
   ```bash
   cd Clientes
   pip install -r requirements.txt
   python PDFgen.py
   ```

### Opção 2: Usar executáveis (Produção)

1. **Compilar o Servidor:**
   ```bash
   cd Servidor
   pyinstaller Iniciar_Servidor.spec
   ```

2. **Compilar o Cliente:**
   ```bash
   cd Clientes
   pyinstaller PDFgen.spec
   ```

## 🌐 Acesso

- **Painel Web:** http://localhost:5000
- **API:** http://localhost:5000/api/pedidos

## 📋 Funcionalidades

### Cliente Desktop (PDFgen.py)
- Interface gráfica intuitiva
- Geração automática de PDFs
- Armazenamento em banco SQLite
- Integração com servidor web
- Validação de dados

### Servidor Web (app.py)
- Painel de gerenciamento web
- API REST para integração
- Banco de dados SQLite
- Interface responsiva
- Controle de status de pedidos

## 🔧 Requisitos

- Python 3.7+
- pip (gerenciador de pacotes)
- Bibliotecas listadas em requirements.txt

## 📝 Licença

Projeto para uso interno da Plante Uma Flor Floricultura.