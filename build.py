import sys
from DriverStation import version
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["pygame","time","serial","sys"], "excludes":["absl-py", "aiohttp", "astor", "async-timeout", "chardet", "cx-Freeze", "cycler", "Cython", "discord.py", "future", "gast", "grpcio", "h5py ", "inputs", "iso8601", "Keras", "Keras-Applications", "Keras-Preprocessing", "kiwisolver", "Markdown", "matplotlib", "mock", "multidict", "numpy", "pandas", "pbr", "Pillow", "pip", "protobuf", "psutil", "py4j", "pyglet", "pyparsing", "PyQt5", "PyQt5-sip", "python-dateutil", "pytz", "PyYAML", "rlbot", "scikit-learn", "scipy",  "setuptools", "six", "sklearn", "tensorboard", "tensorflow", "tensorflow-estimator", "termcolor", "torch", "torchvision", "web.py", "websockets", "Werkzeug", "wheel"]}

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name = "MiniFRC Driver Station v%s"%(version),
    version = str(version),
    description = "Driver Station for Bluetooth-controlled robots",
    options = {"build_exe": build_exe_options},
    executables = [Executable("Driverstation.py",base=base)]
    
    
