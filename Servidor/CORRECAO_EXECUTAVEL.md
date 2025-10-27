# 🔧 Correção - Erro ao Executar Gerador_De_Pedidos.exe

## ⚠️ Problema

```
❌ Erro: Arquivo não encontrado: C:\Users\caioc\AppData\Local\Temp\_MEI11002\static\app.py
```

### Causa
O PyInstaller extrai o executável para uma pasta temporária, e o caminho não está sendo resolvido corretamente.

---

## ✅ Solução 1: Modo Onedir (Recomendado)

Em vez de criar um único .exe, vamos criar uma pasta com o executável e os arquivos necessários.

### Novo arquivo .spec (corrigido)

Criar ou atualizar `Servidor/Gerador_De_Pedidos_onedir.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['Gerador_De_Pedidos.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('static', 'static'),
        ('../Clientes/PDFgen.py', 'Clientes'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Gerador_De_Pedidos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    upx_include=[],
    name='Gerador_De_Pedidos'
)
```

### Compilar no modo onedir:

```powershell
cd Servidor
pyinstaller Gerador_De_Pedidos_onedir.spec
```

Isso criará uma pasta `dist/Gerador_De_Pedidos/` com todos os arquivos necessários.

---

## ✅ Solução 2: Executar do Script Python (Temporário)

Enquanto o executável não está funcionando perfeitamente, você pode usar o script Python diretamente:

```powershell
cd Servidor
python Gerador_De_Pedidos.py
```

Isso funciona perfeitamente sem compilar!

---

## 🚀 Solução 3: Estrutura de Pastas Correta

### Para o Executável Funcionar

Os executáveis precisam estar na estrutura correta:

```
GerenciadorDeComandas/
├── Gerador_De_Pedidos.exe  ← Execute daqui
├── Servidor/
│   └── static/
│       └── app.py          ← Arquivos necessários
└── Clientes/
    └── PDFgen.exe
```

**Explicação:**
O executável está em `Servidor/` mas procura arquivos em caminhos relativos. Mova para a raiz ou ajuste os caminhos.

---

## 📝 Arquivo .spec Atualizado

Já foi atualizado para incluir a pasta `static` completa.

Recompile novamente:

```powershell
cd Servidor
pyinstaller Gerador_De_Pedidos.spec
```

---

## 🎯 Solução Rápida (Recomendada)

**Use o script Python diretamente** até compilar corretamente:

```powershell
cd Servidor
python Gerador_De_Pedidos.py
```

Isso vai:
1. ✅ Iniciar o servidor Flask
2. ✅ Abrir o PDFgen
3. ✅ Abrir o navegador
4. ✅ Tudo funcionar perfeitamente!

---

**Desenvolvido para:** Plante Uma Flor Floricultura 🌺

