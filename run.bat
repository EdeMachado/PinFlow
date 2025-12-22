@echo off
chcp 65001 >nul
cls

echo ========================================
echo   📌➜ PinFlow Pro v3.0
echo   Suas tarefas sempre no topo!
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Instale Python 3.8+ em: https://python.org
    pause
    exit /b 1
)

echo [OK] Python encontrado!
echo.
echo Verificando dependencias...

REM Verificar se PySide6 está instalado
python -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo [!] Instalando PySide6...
    pip install -r requirements.txt
) else (
    echo [OK] PySide6 ja instalado!
)

echo.
echo ========================================
echo   Iniciando PinFlow Pro...
echo   (Always On Top ativado!)
echo ========================================
echo.

REM Executar o aplicativo
python main.py 2>&1

if errorlevel 1 (
    echo.
    echo [ERRO] Ocorreu um erro ao executar!
)

pause
