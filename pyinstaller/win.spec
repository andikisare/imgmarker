# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['..\\imgmarker\\__init__.py'],
    pathex=[],
    binaries=[],
    datas=[ ('..\\imgmarker\\heart_clear.ico', '.'), ('..\\imgmarker\\heart_solid.ico', '.'), ('..\\imgmarker\\icon.ico', '.') ],
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
    name='Image Marker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    contents_directory='.',
    icon=['..\\imgmarker\\icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Image Marker',
)
