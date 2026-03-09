@echo off
setlocal

cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 goto :use_py

where python >nul 2>nul
if %errorlevel%==0 goto :use_python

echo Python est introuvable. Installez Python et verifiez le PATH.
exit /b 1

:use_py
py -3 -m pip install -r requirements.txt
if not %errorlevel%==0 (
	echo Echec de l'installation des dependances avec py -3.
	exit /b 1
)
py -3 main.py
exit /b %errorlevel%

:use_python
python -m pip install -r requirements.txt
if not %errorlevel%==0 (
	echo Echec de l'installation des dependances avec python.
	exit /b 1
)
python main.py
exit /b %errorlevel%
