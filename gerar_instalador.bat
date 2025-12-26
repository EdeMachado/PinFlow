@echo off
chcp 65001 >nul
echo ========================================
echo Gerador de Instalador - PinFlow Pro
echo ========================================
echo.

REM Verificar se o executável foi gerado
if not exist "dist\PinFlow_Pro.exe" (
    echo [ERRO] Executável não encontrado!
    echo Por favor, execute primeiro: pyinstaller build.spec --clean --noconfirm
    pause
    exit /b 1
)

echo [OK] Executável encontrado: dist\PinFlow_Pro.exe
echo.

REM Procurar Inno Setup em vários locais
set ISCC_PATH=
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe
) else if exist "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" (
    set ISCC_PATH=C:\Program Files (x86)\Inno Setup 5\ISCC.exe
) else if exist "C:\Program Files\Inno Setup 5\ISCC.exe" (
    set ISCC_PATH=C:\Program Files\Inno Setup 5\ISCC.exe
)

if "%ISCC_PATH%"=="" (
    echo [ERRO] Inno Setup não encontrado!
    echo.
    echo Por favor, instale o Inno Setup:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo Ou informe o caminho manualmente editando este arquivo.
    pause
    exit /b 1
)

echo [OK] Inno Setup encontrado: %ISCC_PATH%
echo.
echo Gerando instalador...
echo.

"%ISCC_PATH%" installer.iss

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo [SUCESSO] Instalador gerado!
    echo ========================================
    echo.
    echo O instalador está em: dist\installer\PinFlow_Pro_Setup.exe
    echo.
    echo Este instalador irá:
    echo   - Instalar em: C:\Program Files\PinFlow Pro
    echo   - Criar atalho no Desktop com ícone do alfinete
    echo   - Abrir a pasta de instalação após instalação
    echo.
) else (
    echo.
    echo [ERRO] Falha ao gerar instalador!
    echo.
)

pause

