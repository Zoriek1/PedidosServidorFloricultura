# 🌸 Plante Uma Flor v2.0 - Servidor

Sistema de gerenciamento de pedidos para floricultura com interface web moderna.

---

## 📁 Estrutura do Projeto

```
Servidor/
│
├── 🚀 run/                    # ARQUIVOS ESSENCIAIS (use aqui!)
│   ├── main.py                # Entry point do servidor
│   ├── config.json            # Configurações
│   ├── requirements.txt       # Dependências Python
│   ├── INICIAR_AQUI.bat       # Iniciar com janela (ver logs)
│   ├── INICIAR_SERVIDOR_BACKGROUND.vbs  # Iniciar em background
│   ├── PARAR_SERVIDOR.bat     # Parar o servidor
│   ├── app/                   # Código da aplicação Flask
│   └── templates/             # Templates HTML
│
├── 💾 static/                  # Arquivos estáticos e banco de dados
│   ├── database.db            # Banco de dados SQLite
│   ├── css/                   # Estilos
│   └── js/                    # JavaScript
│
├── 📝 logs/                    # Logs do servidor
│   └── server_YYYYMMDD.log    # Logs diários
│
├── 📚 docs/                    # Documentação
│   ├── README*.md             # Vários READMEs
│   ├── GUIA_RAPIDO.md         # Guia rápido
│   ├── ESTRUTURA_DO_PROJETO.md
│   └── ...                    # Outros documentos
│
└── 🔧 utils/                   # Utilitários e desenvolvimento
    ├── test_server.py         # Testes automatizados
    ├── migrate_database.py    # Migração de banco de dados
    ├── compilar.bat           # Compilar executáveis
    ├── *.exe                  # Executáveis compilados
    └── build/                 # Arquivos de build do PyInstaller
```

---

## 🚀 Como Usar

### Iniciar o Servidor

Navegue até a pasta `run/` e escolha:

**Opção 1: Com janela do CMD (ver logs)**
```bash
cd run
INICIAR_AQUI.bat
```

**Opção 2: Em background (sem janela)**
```bash
cd run
duplo clique em INICIAR_SERVIDOR_BACKGROUND.vbs
```

### Parar o Servidor

```bash
cd run
PARAR_SERVIDOR.bat
```

### Acessar o Painel

Após iniciar o servidor, acesse:
- **Local:** http://localhost:5000
- **Rede:** http://[SEU_IP]:5000

---

## ⚙️ Configuração

Edite `run/config.json` para alterar:
```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false,
    "broadcast_enabled": true,
    "broadcast_port": 37020
  }
}
```

---

## 📦 Primeira Instalação

1. **Instalar dependências:**
   ```bash
   cd run
   pip install -r requirements.txt
   ```

2. **Iniciar o servidor:**
   ```bash
   python main.py
   ```

3. **Pronto!** Acesse http://localhost:5000

---

## 🛠️ Desenvolvimento

Para desenvolvedores, os utilitários estão em `utils/`:

- **Testar servidor:** `python utils/test_server.py`
- **Migrar banco:** `python utils/migrate_database.py`
- **Compilar:** `utils/compilar.bat`

---

## 📚 Documentação Completa

Toda a documentação está em `docs/`:
- Guias de uso
- Documentação técnica
- Histórico de implementações
- READMEs antigos

---

## 🎯 Dicas

✅ **Use sempre a pasta `/run` para executar o servidor**
✅ **Nunca delete `/static` (contém o banco de dados!)**  
✅ **Logs ficam em `/logs` - limpe periodicamente**
✅ **Consulte `/docs` se precisar de ajuda detalhada**

---

## 🆘 Problemas Comuns

### Erro: "ModuleNotFoundError"
**Solução:**
```bash
cd run
pip install -r requirements.txt
```

### Erro: "Port 5000 already in use"
**Solução:**
```bash
cd run
PARAR_SERVIDOR.bat
```
Aguarde 5 segundos e tente novamente.

### Servidor não inicia
**Solução:**
1. Use `INICIAR_AQUI.bat` para ver os erros
2. Verifique se o Python está instalado: `python --version`
3. Verifique os logs em `/logs`

---

## 📞 Suporte

Para mais informações, consulte:
- `/docs/GUIA_RAPIDO.md`
- `/docs/COMO_USAR_BACKGROUND.md`
- `/docs/ESTRUTURA_DO_PROJETO.md`

---

**Plante Uma Flor v2.0** 🌸  
Sistema de Gerenciamento de Pedidos


