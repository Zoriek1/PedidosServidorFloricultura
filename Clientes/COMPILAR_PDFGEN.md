# 🔨 Como Compilar o PDFgen.exe

## 📋 Pré-requisitos

### 1. Instalar PyInstaller

```powershell
pip install pyinstaller
```

### 2. Instalar Dependências

```powershell
cd Clientes
pip install -r requirements.txt
```

---

## 🔨 Compilar

### Opção 1: Usando o Arquivo .spec

```powershell
cd Clientes
pyinstaller PDFgen.spec
```

O arquivo será criado em: `Clientes/dist/PDFgen.exe`

### Opção 2: PyInstaller Direto

```powershell
cd Clientes
pyinstaller --onefile --console --name=PDFgen --icon=Buques.ico --add-data "Montserrat-VariableFont_wght.ttf;." --add-data "Montserrat-Italic-VariableFont_wght.ttf;." --add-data "Raleway-VariableFont_wght.ttf;." --add-data "Raleway-Italic-VariableFont_wght.ttf;." --add-data "Buques.ico;." PDFgen.py
```

---

## 📁 Estrutura Após Compilação

```
Clientes/
├── dist/
│   └── PDFgen.exe  ← Executável gerado
├── build/ (temporários)
├── PDFgen.py
├── PDFgen.spec
└── fontes/ (incluídas no .exe)
```

---

## ✅ Checklist

- [ ] PyInstaller instalado
- [ ] Dependências instaladas
- [ ] Arquivo .spec criado
- [ ] Compilação executada
- [ ] PDFgen.exe testado

---

**Desenvolvido para:** Plante Uma Flor Floricultura 🌺

