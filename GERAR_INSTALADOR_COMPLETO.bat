@echo off
chcp 65001 >nul
echo ========================================
echo GERADOR DE INSTALADOR - PinFlow Pro
echo ========================================
echo.

REM Verificar se o executável existe
if not exist "dist\PinFlow_Pro.exe" (
    echo [ERRO] Executável não encontrado!
    echo.
    echo Gerando executável primeiro...
    echo.
    pyinstaller build.spec --clean --noconfirm
    echo.
    if not exist "dist\PinFlow_Pro.exe" (
        echo [ERRO] Falha ao gerar executável!
        pause
        exit /b 1
    )
)

echo [OK] Executável verificado: dist\PinFlow_Pro.exe
echo.

REM Criar pasta para o instalador
if not exist "dist\installer" mkdir "dist\installer"
echo [OK] Pasta criada: dist\installer
echo.

REM Copiar arquivos necessários para o instalador
echo Copiando arquivos para o instalador...
copy /Y "dist\PinFlow_Pro.exe" "dist\installer\" >nul
copy /Y "valid_licenses.json" "dist\installer\" >nul 2>&1
copy /Y "alfinete_verde.ico" "dist\installer\" >nul 2>&1
xcopy /E /I /Y "i18n" "dist\installer\i18n\" >nul 2>&1
echo [OK] Arquivos copiados
echo.

REM Criar script de instalação
echo Criando script de instalação...
(
echo @echo off
echo chcp 65001 ^>nul
echo echo ========================================
echo echo Instalador PinFlow Pro
echo echo ========================================
echo echo.
echo.
echo REM Verificar se está executando como administrador
echo net session ^>nul 2^>^&1
echo if %%errorLevel%% neq 0 ^(
echo     echo [AVISO] Este instalador precisa de privilégios de administrador.
echo     echo Por favor, execute como Administrador ^(botão direito ^> Executar como administrador^)
echo     pause
echo     exit /b 1
echo ^)
echo.
echo set "INSTALL_DIR=C:\Program Files\PinFlow Pro"
echo set "DESKTOP=%%USERPROFILE%%\Desktop"
echo set "EXE_NAME=PinFlow_Pro.exe"
echo.
echo echo Instalando PinFlow Pro...
echo echo.
echo.
echo REM Criar diretório de instalação
echo if not exist "%%INSTALL_DIR%%" ^(
echo     mkdir "%%INSTALL_DIR%%"
echo     echo [OK] Diretório criado: %%INSTALL_DIR%%
echo ^)
echo.
echo REM Copiar executável
echo copy /Y "%%~dp0%%EXE_NAME%%" "%%INSTALL_DIR%%\%%EXE_NAME%%" ^>nul
echo echo [OK] Executável instalado
echo.
echo REM Copiar arquivos necessários
echo if exist "%%~dp0valid_licenses.json" ^(
echo     copy /Y "%%~dp0valid_licenses.json" "%%INSTALL_DIR%%\" ^>nul
echo     echo [OK] Arquivo de licenças copiado
echo ^)
echo.
echo if exist "%%~dp0alfinete_verde.ico" ^(
echo     copy /Y "%%~dp0alfinete_verde.ico" "%%INSTALL_DIR%%\" ^>nul
echo     echo [OK] Ícone copiado
echo ^)
echo.
echo REM Copiar pasta i18n
echo if exist "%%~dp0i18n" ^(
echo     xcopy /E /I /Y "%%~dp0i18n" "%%INSTALL_DIR%%\i18n\" ^>nul
echo     echo [OK] Traduções copiadas
echo ^)
echo.
echo REM Criar atalho no Desktop
echo set "SHORTCUT=%%DESKTOP%%\PinFlow Pro.lnk"
echo powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%%SHORTCUT%%'); $Shortcut.TargetPath = '%%INSTALL_DIR%%\%%EXE_NAME%%'; $Shortcut.WorkingDirectory = '%%INSTALL_DIR%%'; $Shortcut.IconLocation = '%%INSTALL_DIR%%\%%EXE_NAME%%'; $Shortcut.Description = 'PinFlow Pro - Kanban Board'; $Shortcut.Save()"
echo echo [OK] Atalho criado no Desktop com ícone do alfinete
echo.
echo REM Criar entrada no Menu Iniciar
echo set "START_MENU=%%APPDATA%%\Microsoft\Windows\Start Menu\Programs"
echo set "START_SHORTCUT=%%START_MENU%%\PinFlow Pro.lnk"
echo powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%%START_SHORTCUT%%'); $Shortcut.TargetPath = '%%INSTALL_DIR%%\%%EXE_NAME%%'; $Shortcut.WorkingDirectory = '%%INSTALL_DIR%%'; $Shortcut.IconLocation = '%%INSTALL_DIR%%\%%EXE_NAME%%'; $Shortcut.Description = 'PinFlow Pro - Kanban Board'; $Shortcut.Save()"
echo echo [OK] Entrada criada no Menu Iniciar
echo.
echo echo.
echo echo ========================================
echo echo [SUCESSO] Instalação concluída!
echo echo ========================================
echo echo.
echo echo PinFlow Pro foi instalado em:
echo echo %%INSTALL_DIR%%
echo echo.
echo echo Um atalho foi criado na Área de Trabalho com o ícone do alfinete.
echo echo.
echo echo Abrindo pasta de instalação...
echo start "" "%%INSTALL_DIR%%"
echo echo.
echo pause
) > "dist\installer\INSTALAR.bat"

echo [OK] Script de instalação criado
echo.

REM Criar arquivo README
(
echo PinFlow Pro - Instalador
echo ========================
echo.
echo Para instalar:
echo 1. Execute INSTALAR.bat como Administrador ^(botão direito ^> Executar como administrador^)
echo 2. O programa será instalado em: C:\Program Files\PinFlow Pro
echo 3. Um atalho será criado na Área de Trabalho com o ícone do alfinete
echo 4. A pasta de instalação será aberta automaticamente
echo.
echo Arquivos incluídos:
echo - PinFlow_Pro.exe ^(Executável principal^)
echo - valid_licenses.json ^(Licenças válidas^)
echo - alfinete_verde.ico ^(Ícone^)
echo - i18n\ ^(Traduções^)
echo.
echo © 2025 - Criado por Ede Machado
) > "dist\installer\LEIA-ME.txt"

echo [OK] Arquivo README criado
echo.

echo ========================================
echo [SUCESSO] Instalador gerado!
echo ========================================
echo.
echo Localização: dist\installer\
echo.
echo Arquivos incluídos:
dir /B "dist\installer"
echo.
echo Para instalar:
echo 1. Vá para: dist\installer\
echo 2. Execute INSTALAR.bat como Administrador
echo.
pause

