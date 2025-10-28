# -*- mode: python ; coding: utf-8 -*-
# PDFgen.py - Plante Uma Flor v2.0
# Spec file para PyInstaller com descoberta automática de rede

a = Analysis(
    ['PDFgen.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Montserrat-VariableFont_wght.ttf', '.'),
        ('Montserrat-Italic-VariableFont_wght.ttf', '.'),
        ('Raleway-VariableFont_wght.ttf', '.'),
        ('Raleway-Italic-VariableFont_wght.ttf', '.'),
        ('Buques.ico', '.'),
    ],
    hiddenimports=['reportlab', 'requests', 'socket', 'json'],
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
    a.binaries,
    a.datas,
    [],
    name='PDFgen',
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
    icon='Buques.ico',
)
