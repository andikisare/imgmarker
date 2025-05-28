# -*- mode: python ; coding: utf-8 -*-

import sys
sys.path.insert(0, '../')
import imgmarker
from PyInstaller.utils.hooks import collect_submodules, collect_data_files, collect_dynamic_libs

hiddenimports = collect_submodules('imgmarker') 
datas = collect_data_files('imgmarker') 
for i, _ in enumerate(datas):
    datas[i] = (datas[i][0], datas[i][1].replace('imgmarker','.'))

binaries = collect_dynamic_libs('imgmarker')

a = Analysis(
    ['../imgmarker/__main__.py'],
    pathex=['../'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    icon=['../imgmarker/icon.ico'],
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
app = BUNDLE(
    coll,
    name='Image Marker.app',
    icon='../imgmarker/icon.ico',
    bundle_identifier=None,
)
