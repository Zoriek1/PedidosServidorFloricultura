# 🚀 Como Executar o Plante Uma Flor v2.0

## ❌ Problema Identificado
O erro `[WinError 2] O sistema não pode encontrar o arquivo especificado` indica que o PyInstaller não está instalado.

## ✅ Soluções Disponíveis

### **Opção 1: Script Automático (Recomendado)**

Execute um dos scripts abaixo:

**Windows (CMD):**
```cmd
install_and_build.bat
```

**Windows (PowerShell):**
```powershell
.\install_and_build.ps1
```

### **Opção 2: Instalação Manual**

1. **Instalar dependências:**
```cmd
pip install pyinstaller reportlab requests flask flask-sqlalchemy werkzeug
```

2. **Executar build simplificado:**
```cmd
cd client\src\build
python build_simple.py
```

### **Opção 3: Executar sem Build (Desenvolvimento)**

Se quiser testar sem criar executável:

1. **Instalar dependências:**
```cmd
pip install reportlab requests flask flask-sqlalchemy werkzeug
```

2. **Executar cliente:**
```cmd
cd client
python src\main.py
```

3. **Executar servidor:**
```cmd
cd server
python src\main.py
```

## 🔧 Troubleshooting

### **Erro: "Python não encontrado"**
- Instale Python 3.7+ de https://www.python.org/downloads/
- Marque "Add Python to PATH" durante a instalação

### **Erro: "pip não encontrado"**
```cmd
python -m ensurepip --upgrade
```

### **Erro: "Permissão negada"**
- Execute como Administrador
- Ou use: `pip install --user pyinstaller`

### **Erro: "Módulo não encontrado"**
```cmd
pip install --upgrade pip
pip install pyinstaller reportlab requests
```

## 📁 Estrutura Após Build

```
plante-uma-flor-v2/
├── dist/
│   ├── PlanteUmaFlor-Client.exe    # Executável principal
│   ├── Iniciar_Cliente.bat         # Script de inicialização
│   └── resources/                   # Recursos necessários
├── client/                          # Código fonte do cliente
├── server/                          # Código fonte do servidor
└── docs/                           # Documentação
```

## 🎯 Próximos Passos

1. **Execute o script de instalação**
2. **Aguarde a instalação das dependências**
3. **Aguarde a criação do executável**
4. **Execute `Iniciar_Cliente.bat` para usar o aplicativo**

## 📞 Suporte

Se ainda tiver problemas:

1. Verifique se o Python está instalado: `python --version`
2. Verifique se o pip está funcionando: `pip --version`
3. Execute: `pip install --upgrade pip`
4. Tente novamente o script de instalação

---

**💡 Dica:** O script `build_simple.py` é mais robusto e instala automaticamente as dependências necessárias.