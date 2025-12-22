@echo off
echo ========================================
echo   INSTALAR INICIALIZACAO AUTOMATICA
echo   Post-it Kanban Pro
echo ========================================
echo.

REM Caminho atual do projeto
set CURRENT_DIR=%~dp0

REM Caminho da pasta Startup do Windows
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

echo Pasta do projeto: %CURRENT_DIR%
echo Pasta Startup: %STARTUP_FOLDER%
echo.

REM Criar atalho usando PowerShell
echo Criando atalho na pasta Inicializar...

powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTUP_FOLDER%\PostitKanban.lnk'); $Shortcut.TargetPath = '%CURRENT_DIR%run_startup.bat'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.IconLocation = 'shell32.dll,165'; $Shortcut.Description = 'Post-it Kanban Pro - Inicia automaticamente'; $Shortcut.Save()"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   SUCESSO!
    echo ========================================
    echo.
    echo O Kanban vai abrir AUTOMATICAMENTE
    echo sempre que voce ligar o computador!
    echo.
    echo Igual ao Post-it do Windows!
    echo.
    echo Atalho criado em:
    echo %STARTUP_FOLDER%\PostitKanban.lnk
    echo.
    echo ========================================
    echo   TESTE AGORA:
    echo ========================================
    echo.
    echo 1. Feche o Kanban se estiver aberto
    echo 2. Execute run_startup.bat para testar
    echo 3. Ou reinicie o PC!
    echo.
) else (
    echo.
    echo [ERRO] Nao foi possivel criar o atalho!
    echo Execute como Administrador.
    echo.
)

pause




