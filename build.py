from distutils.core import setup
import py2exe, sys, glob

sys.argv.append('py2exe')

setup(
    data_files = [("Resources", glob.glob('Resources/*'))],
    options = {
        'py2exe': {
            "optimize": 2,
            "dist_dir": "Havok OpenFlight Converter",
            "dll_excludes": ["MSVCP90.dll"]
        }
    },
    windows=[{'script': "HavokOpenFlightConverter.py", "icon_resources": [(1, "Resources/havok.ico")]}],
    zipfile=None,
)
