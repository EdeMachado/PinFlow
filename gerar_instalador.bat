@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║     PINFLOW PRO - GERADOR DE INSTALADOR PROFISSIONAL     ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [ETAPA 1/5] Verificando Python...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não encontrado!
    echo    Instale Python 3.8+ de https://www.python.org
    pause
    exit /b 1
)
echo ✓ Python encontrado!
echo.

REM ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [ETAPA 2/5] Instalando PyInstaller...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
python -m pip install --upgrade pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO ao instalar PyInstaller!
    pause
    exit /b 1
)
echo ✓ PyInstaller instalado!
echo.

REM ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [ETAPA 3/5] Gerando executável com PyInstaller...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo    Isso pode demorar alguns minutos...
echo.

REM Limpar builds anteriores
if exist "build" rmdir /s /q "build"
if exist "dist\PinFlow_Pro" rmdir /s /q "dist\PinFlow_Pro"

REM Gerar executável
pyinstaller --clean build.spec
if errorlevel 1 (
    echo ❌ ERRO ao gerar executável!
    echo    Verifique o arquivo build.spec
    pause
    exit /b 1
)
echo ✓ Executável gerado em: dist\PinFlow_Pro\
echo.

REM ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [ETAPA 4/5] Verificando Inno Setup...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if not exist "%INNO_PATH%" (
    echo ⚠️  Inno Setup não encontrado!
    echo.
    echo    Para gerar o instalador, você precisa:
    echo    1. Baixar Inno Setup 6: https://jrsoftware.org/isdl.php
    echo    2. Instalar em: C:\Program Files (x86)\Inno Setup 6\
    echo    3. Executar este script novamente
    echo.
    echo ✓ Executável já está pronto em: dist\PinFlow_Pro\PinFlow_Pro.exe
    echo.
    pause
    exit /b 0
)
echo ✓ Inno Setup encontrado!
echo.

REM ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [ETAPA 5/5] Gerando instalador com Inno Setup...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo    Compilando instalador...
echo.

"%INNO_PATH%" "installer.iss"
if errorlevel 1 (
    echo ❌ ERRO ao gerar instalador!
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                   ✓ CONCLUÍDO COM SUCESSO!               ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo 📦 INSTALADOR GERADO:
echo    dist\installer\PinFlow_Pro_Setup.exe
echo.
echo 🚀 PRONTO PARA DISTRIBUIR!
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Próximos passos:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 1. Teste o instalador: dist\installer\PinFlow_Pro_Setup.exe
echo 2. Distribua para seus clientes
echo 3. Venda por R$ 9,99!
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
pause
explorer "dist\installer"

