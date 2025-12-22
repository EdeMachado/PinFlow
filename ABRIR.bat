@echo off
cd /d "%~dp0"
python main.py
if errorlevel 1 (
    echo.
    echo ERRO: Nao foi possivel iniciar o sistema.
    echo Verifique se o Python esta instalado.
    pause
)

