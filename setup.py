from cx_Freeze import setup, Executable
import os

base = "Win32GUI"

includefiles = ["QSS","Images","links.json","icons","modules","LICENSE"] #copy needed files

excludes = ["asyncio","concurrent","lib2to3","multiprocessing","pydoc_data","unittest","distutils","test","tkinter","snoop","PySide6","PyQt5"]  #unneeded packages

packages = ["PySide2","urllib","bs4","io","PIL","requests","favicon","hashlib","webbrowser","json","os"]  #include python packages


inst_dir = os.path.join(r"C:\Users",os.getlogin(),r"Appdata\Local\Programs\Usehan")

#BDIST_MSI -> make MSI windows installer
bdist_msi_options = {
    "all_users": True,
    "initial_target_dir": inst_dir}

#BUILD_EXE -> create an executable application
build_exe_options = {
    "packages": packages,
    "include_files": includefiles,
    "excludes": excludes,}

#FINAL EXECUTABLE FILE PROPERTIES
target = Executable(
    script = "MainWindow.py",
    base = base,
    icon = "Images\\Usehan.ico",
    target_name = "Usehan.exe")

setup(  name = "Usehan",
        version = "0.2",
        description = "URL session handler",
        executables = [target],
        options = {
            "build_exe": build_exe_options,
            "bdist_msi": bdist_msi_options})