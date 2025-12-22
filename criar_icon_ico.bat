@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║        PINFLOW PRO - CRIAR ÍCONE .ICO                     ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo Este script ajuda você a criar o arquivo icon.ico
echo.
echo OPCOES:
echo.
echo 1. Converter icon.png para .ico online (RECOMENDADO)
echo    - Abrir: https://convertio.co/pt/png-ico/
echo    - Upload: icon.png
echo    - Converter e baixar como: icon.ico
echo    - Salvar na pasta do projeto
echo.
echo 2. Usar ImageMagick (se instalado)
echo    - Comando: magick convert icon.png -define icon:auto-resize=256,128,64,48,32,16 icon.ico
echo.
echo 3. Verificar se icon.ico já existe
echo.

if exist "icon.ico" (
    echo [OK] icon.ico ja existe!
    echo.
    dir icon.ico
    echo.
    pause
    exit /b 0
)

if not exist "icon.png" (
    echo [ERRO] icon.png nao encontrado!
    echo.
    echo Execute primeiro: python criar_icone.py
    echo.
    pause
    exit /b 1
)

echo [INFO] icon.png encontrado!
echo.
echo Para criar icon.ico:
echo.
echo OPCAO 1 - ONLINE (MAIS FACIL):
echo   1. Abrir: https://convertio.co/pt/png-ico/
echo   2. Fazer upload de: icon.png
echo   3. Converter para .ico
echo   4. Baixar e salvar como: icon.ico
echo.
echo OPCAO 2 - IMAGEMAGICK:
echo   magick convert icon.png -define icon:auto-resize=256,128,64,48,32,16 icon.ico
echo.
echo Depois de criar icon.ico, execute: gerar_instalador.bat
echo.
pause

