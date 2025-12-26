@echo off
chcp 65001 >nul
echo ========================================
echo Instalador PinFlow Pro
echo ========================================
echo.

REM Verificar se está executando como administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [AVISO] Este instalador precisa de privilégios de administrador.
    echo Por favor, execute como Administrador (botão direito ^> Executar como administrador)
    pause
    exit /b 1
)

set "INSTALL_DIR=C:\Program Files\PinFlow Pro"
set "DESKTOP=%USERPROFILE%\Desktop"
set "EXE_NAME=PinFlow_Pro.exe"

echo Instalando PinFlow Pro...
echo.

REM Criar diretório de instalação
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo [OK] Diretório criado: %INSTALL_DIR%
)

REM Copiar executável
if exist "dist\%EXE_NAME%" (
    copy /Y "dist\%EXE_NAME%" "%INSTALL_DIR%\%EXE_NAME%" >nul
    echo [OK] Executável copiado
) else (
    echo [ERRO] Executável não encontrado em dist\%EXE_NAME%
    pause
    exit /b 1
)

REM Copiar arquivos necessários
if exist "valid_licenses.json" (
    copy /Y "valid_licenses.json" "%INSTALL_DIR%\" >nul
    echo [OK] Arquivo de licenças copiado
)

if exist "alfinete_verde.ico" (
    copy /Y "alfinete_verde.ico" "%INSTALL_DIR%\" >nul
    echo [OK] Ícone copiado
)

REM Copiar pasta i18n
if exist "i18n" (
    xcopy /E /I /Y "i18n" "%INSTALL_DIR%\i18n\" >nul
    echo [OK] Traduções copiadas
)

REM Criar atalho no Desktop
set "SHORTCUT=%DESKTOP%\PinFlow Pro.lnk"
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\%EXE_NAME%'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%INSTALL_DIR%\%EXE_NAME%'; $Shortcut.Description = 'PinFlow Pro - Kanban Board'; $Shortcut.Save()"
echo [OK] Atalho criado no Desktop

REM Criar entrada no Menu Iniciar
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "START_SHORTCUT=%START_MENU%\PinFlow Pro.lnk"
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\%EXE_NAME%'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%INSTALL_DIR%\%EXE_NAME%'; $Shortcut.Description = 'PinFlow Pro - Kanban Board'; $Shortcut.Save()"
echo [OK] Entrada criada no Menu Iniciar

echo.
echo ========================================
echo [SUCESSO] Instalação concluída!
echo ========================================
echo.
echo PinFlow Pro foi instalado em:
echo %INSTALL_DIR%
echo.
echo Um atalho foi criado na Área de Trabalho com o ícone do alfinete.
echo.
echo Abrindo pasta de instalação...
start "" "%INSTALL_DIR%"
echo.
pause

