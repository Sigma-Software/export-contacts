@echo off
pyinstaller --onefile --windowed --hidden-import="pkg_resources.py2_warn" -i="../src/ui/styles/common/logo.ico" -n="ExportContacts tool" ../src/main.py