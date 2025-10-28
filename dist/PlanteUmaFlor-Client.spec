# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\Pichau\\Downloads\\1\\PedidosServidorFloricultura\\plante-uma-flor-v2\\client\\src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\Pichau\\Downloads\\1\\PedidosServidorFloricultura\\plante-uma-flor-v2\\client\\src\\resources\\config.json', 'resources')],
    hiddenimports=['reportlab', 'reportlab.pdfgen', 'reportlab.pdfgen.canvas', 'reportlab.lib', 'reportlab.lib.pagesizes', 'reportlab.lib.units', 'reportlab.pdfbase', 'reportlab.pdfbase.pdfmetrics', 'reportlab.pdfbase.ttfonts', 'requests', 'sqlite3', 'tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'tkinter.filedialog', 'pathlib', 'datetime', 'json'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    name='PlanteUmaFlor-Client',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
