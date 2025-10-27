# 🚀 Como Compilar os Executáveis .exe

## 📋 Pré-requisitos

### 1. Instalar PyInstaller

```powershell
pip install pyinstaller
```

### 2. Instalar Dependências do Projeto

```powershell
cd Servidor\static
pip install -r requirements.txt
```

---

## 🔨 Compilar os Executáveis

### Opção 1: Usando os Arquivos .spec (Recomendado)

#### Gerar Gerador_De_Pedidos.exe

```powershell
cd Servidor
pyinstaller Gerador_De_Pedidos.spec
```

O arquivo será criado em: `Servidor/dist/Gerador_De_Pedidos.exe`

#### Gerar Iniciar_Servidor.exe

```powershell
cd Servidor
pyinstaller Iniciar_Servidor.spec
```

O arquivo será criado em: `Servidor/dist/Iniciar_Servidor.exe`

### Opção 2: Via PyInstaller Direto

#### Gerador_De_Pedidos.exe

```powershell
cd Servidor
pyinstaller --onefile --console --name=Gerador_De_Pedidos --icon=Buques.ico Gerador_De_Pedidos.py
```

#### Iniciar_Servidor.exe

```powershell
cd Servidor
pyinstaller --onefile --console --name=Iniciar_Servidor --icon=Buques.ico Iniciar_Servidor.py
```

---

## 📁 Estrutura Após Compilação

```
Servidor/
├── dist/
│   ├── Gerador_De_Pedidos.exe  ← Executável gerado
│   └── Iniciar_Servidor.exe    ← Executável gerado
├── build/
│   └── ... (arquivos temporários)
├── Gerador_De_Pedidos.py
├── Iniciar_Servidor.py
├── Gerador_De_Pedidos.spec
└── Iniciar_Servidor.spec
```

---

## 🎯 Como Usar os Executáveis

### Gerador_De_Pedidos.exe

**Uso:**
1. Execute `Gerador_De_Pedidos.exe`
2. Servidor Flask inicia automaticamente
3. Mantenha a janela aberta
4. Servidor reinicia automaticamente se cair

**Características:**
- ✅ Inicia servidor Flask automaticamente
- ✅ Abre navegador automaticamente
- ✅ Mostra logs em tempo real
- ✅ Reinicia se o servidor cair
- ✅ Funciona 24/7

### Iniciar_Servidor.exe

**Uso:**
1. Execute `Iniciar_Servidor.exe`
2. Se já são 08:00 ou depois → inicia imediatamente
3. Se ainda não são 08:00 → aguarda até 08:00
4. Monitora continuamente
5. Encerra automaticamente às 18:30

**Características:**
- ✅ Inicia às 08:00 automaticamente
- ✅ Inicia imediatamente se for após 08:00
- ✅ Encerra às 18:30
- ✅ Reinicia se o servidor cair
- ✅ Monitora continuamente

---

## 🚀 Compilação Automatizada

Crie um script batch para compilar tudo:

### compilar.bat

```batch
@echo off
echo Compilando executaveis...

pyinstaller Gerador_De_Pedidos.spec
pyinstaller Iniciar_Servidor.spec

echo.
echo Executaveis criados em: dist\
pause
```

Execute:
```powershell
cd Servidor
.\compilar.bat
```

---

## 🐛 Resolver Problemas de Compilação

### Erro: "PyInstaller não encontrado"

```powershell
pip install pyinstaller
```

### Erro: "Módulo não encontrado"

Certifique-se de instalar todas as dependências:

```powershell
pip install flask flask-sqlalchemy werkzeug
```

### Arquivo .exe muito grande

Adicione ao .spec:

```python
excludes=['matplotlib', 'scipy', 'pandas', 'numpy', 'pytest', 'IPython']
```

---

## 📝 Distribuição

### Copiar Arquivos Necessários

Os executáveis precisam estar junto com:

```
📦 Pasta de Distribuição/
├── Gerador_De_Pedidos.exe
├── Iniciar_Servidor.exe
└── Servidor/
    └── static/
        ├── app.py
        ├── requirements.txt
        └── database.db (será criado automaticamente)
```

### Executáveis Standalone

Os executáveis gerados são standalone, mas precisam:
- Python instalado na máquina
- OU usar PyInstaller com `--onefile --onedir` para incluir tudo

---

## ✅ Checklist de Compilação

- [ ] PyInstaller instalado
- [ ] Dependências instaladas
- [ ] Arquivo .spec criado
- [ ] Comando de compilação executado
- [ ] Executáveis testados
- [ ] Distribuição preparada

---

**Desenvolvido para:** Plante Uma Flor Floricultura 🌺

