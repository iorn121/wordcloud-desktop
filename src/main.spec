# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

import sys 
myLibPath = './libs'
sys.path.append(myLibPath)

PATHEX = [os.path.dirname(os.path.abspath(SPEC))]
a = Analysis(
    ['main.py'],
    pathex=PATHEX,
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    Tree('img',prefix='img'),
    Tree('output',prefix='output'),
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='createWordCloud',
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
    icon=['img/Jellyfish-Icon.png'],
)
app = BUNDLE(
    exe,
    name='createWordCloud.app',
    icon='./img/Jellyfish-Icon.png',
    bundle_identifier=None,
)

