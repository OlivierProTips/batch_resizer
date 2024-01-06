# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['batch_resizer_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('venv/lib/python3.11/site-packages/customtkinter', 'customtkinter'),
            ('venv/lib/python3.11/site-packages/darkdetect', 'darkdetect'),
            ('venv/lib/python3.11/site-packages/progress', 'progress')],
    hiddenimports=['tkinter.font', 'tkinter.ttk'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='batch_resizer_gui',
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