@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║     CRIAR ATALHO NA ÁREA DE TRABALHO - PINFLOW PRO       ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

set "EXE_PATH=%~dp0dist\PinFlow_Pro.exe"

REM Obter caminho da área de trabalho usando PowerShell
for /f "delims=" %%i in ('powershell -Command "[System.Environment]::GetFolderPath('Desktop')"') do set "DESKTOP=%%i"
set "SHORTCUT=%DESKTOP%\PinFlow Pro.lnk"

if not exist "%EXE_PATH%" (
    echo ❌ ERRO: Executável não encontrado em:
    echo    %EXE_PATH%
    echo.
    echo    Execute este script da pasta do projeto!
    pause
    exit /b 1
)

echo Criando atalho na área de trabalho...
echo.

REM Usar PowerShell para criar o atalho
powershell -NoProfile -ExecutionPolicy Bypass -Command "$desktop = [System.Environment]::GetFolderPath('Desktop'); $exePath = '%EXE_PATH%'; $shortcutPath = Join-Path $desktop 'PinFlow Pro.lnk'; $WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut($shortcutPath); $Shortcut.TargetPath = $exePath; $Shortcut.WorkingDirectory = [System.IO.Path]::GetDirectoryName($exePath); $Shortcut.IconLocation = $exePath; $Shortcut.Description = 'PinFlow Pro - Sistema de Gerenciamento Kanban'; $Shortcut.Save(); Write-Host 'Atalho criado em:' $shortcutPath"

if exist "%SHORTCUT%" (
    echo ✓ Atalho criado com sucesso!
    echo    Localização: %SHORTCUT%
    echo.
    echo 🎉 Pronto! Você pode encontrar o atalho na sua área de trabalho.
) else (
    echo ❌ Erro ao criar atalho.
)

echo.
pause

