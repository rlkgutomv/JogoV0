import cx_Freeze

executaveis = [
    cx_Freeze.Executable(script="main.py", icon="recursos/assets/icone.png")
]

cx_Freeze.setup(
    name="Fred esquivo esquivo",
    options={
        "build_exe": {
            "packages": ["pygame", "tkinter", "pyttsx3"],
            "include_files": ["recursos", "log.dat"]
        }
    },
    executables=executaveis
)
# python setup.py build
# python setup.py bdist_msi