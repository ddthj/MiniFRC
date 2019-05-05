import sys,os
from cx_Freeze import setup, Executable

#os.environ['TCL_LIBRARY'] = "C:\\Users\\Theddthj\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tcl8.6"
#os.environ['TK_LIBRARY'] = "C:\\Users\\Theddthj\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tk8.6"
os.environ['TCL_LIBRARY'] = "C:\\Program Files (x86)\\Microsoft Visual Studio\\Shared\\Python36_64\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Program Files (x86)\\Microsoft Visual Studio\\Shared\\Python36_64\\tcl\\tk8.6"

#C:\\Users\\Theddthj\\Desktop\\Code\\Python\\MiniFRC

build_exe_options = {"build_exe": "C:\\Users\\Owner\\Desktop\\Code\\Repositories\\MiniFRC", "packages": ["pygame","time","serial","sys"],"excludes":["absl-py", "aiohttp", "astor", "async-timeout", "chardet", "cx-Freeze", "cycler", "Cython", "discord.py", "gast", "grpcio", "h5py ", "inputs", "Keras", "Keras-Applications", "Keras-Preprocessing", "kiwisolver", "Markdown", "matplotlib", "mock", "multidict", "numpy", "pandas", "pbr", "Pillow", "pip", "protobuf", "psutil", "py4j", "pyglet", "pyparsing", "PyQt5", "PyQt5-sip", "python-dateutil", "pytz", "PyYAML", "rlbot", "scikit-learn", "scipy",  "setuptools", "six", "sklearn", "tensorboard", "tensorflow", "tensorflow-estimator", "termcolor", "torch", "torchvision", "web.py", "websockets", "Werkzeug", "wheel"]}

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name = "MiniFRC Driver Station v%s"%(4.1),
    version = 4.1,
    description = "Driver Station for Bluetooth-controlled robots",
    options = {"build_exe": build_exe_options},
    executables = [Executable("DriverStation.py",base=base)])
    
    
