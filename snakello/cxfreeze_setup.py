import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["idna"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
setup(  name = "snakello",
        version = "0.0.1",
        description = "My Snakello in EXE",
        options = {"build_exe": build_exe_options},
        executables = [Executable("..\snakello\snakello.py")])