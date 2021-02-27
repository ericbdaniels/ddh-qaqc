# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os
import site 

site_pkgs_dir = site.getsitepackages()[1]
addl_pkgs = ["plotly", "dash_renderer","dash_html_components","dash_bootstrap_components", "dash_core_components", "dash_table"]

a = Analysis(['main.py'],
             pathex=['c:\\code-dev\\ddh-qaqc\\App'],
             binaries=[],
             datas=[(os.path.join(site_pkgs_dir,pkg),pkg) for pkg in addl_pkgs],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='ddh-qaqc',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='DDH-QAQC')
