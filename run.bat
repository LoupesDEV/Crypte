@echo off
setlocal

cd /d "%~dp0"

py -3 main.py
if %errorlevel%==0 goto :eof

python main.py
if %errorlevel%==0 goto :eof

echo Python est introuvable. Installez Python et verifiez le PATH.
exit /b 1
