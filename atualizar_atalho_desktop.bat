@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║     ATUALIZAR ATALHO DO DESKTOP - PINFLOW PRO           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Obter caminho da área de trabalho
for /f "delims=" %%i in ('powershell -Command "[System.Environment]::GetFolderPath('Desktop')"') do set "DESKTOP=%%i"
set "SHORTCUT=%DESKTOP%\PinFlow Pro.lnk"

REM Verificar se o atalho existe
if not exist "%SHORTCUT%" (
    echo [AVISO] Atalho não encontrado no Desktop.
    echo Criando novo atalho...
    echo.
    goto :CREATE
)

echo Atalho encontrado. Atualizando...
echo.

:CREATE
REM Caminho do executável atualizado
set "EXE_PATH=%~dp0dist\PinFlow_Pro.exe"

if not exist "%EXE_PATH%" (
    echo ❌ ERRO: Executável não encontrado em:
    echo    %EXE_PATH%
    echo.
    echo    Execute este script da pasta do projeto após gerar o executável!
    pause
    exit /b 1
)

REM Atualizar ou criar atalho usando PowerShell
powershell -NoProfile -ExecutionPolicy Bypass -Command "$desktop = [System.Environment]::GetFolderPath('Desktop'); $exePath = '%EXE_PATH%'; $shortcutPath = Join-Path $desktop 'PinFlow Pro.lnk'; $WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut($shortcutPath); $Shortcut.TargetPath = $exePath; $Shortcut.WorkingDirectory = [System.IO.Path]::GetDirectoryName($exePath); $iconPath = Join-Path ([System.IO.Path]::GetDirectoryName($exePath)) 'alfinete_vermelho.ico'; if ([System.IO.File]::Exists($iconPath)) { $Shortcut.IconLocation = $iconPath; } else { $Shortcut.IconLocation = $exePath; }; $Shortcut.Description = 'PinFlow Pro - Sistema de Gerenciamento Kanban'; $Shortcut.Save(); Write-Host '✓ Atalho atualizado com sucesso!' -ForegroundColor Green; Write-Host ''; Write-Host 'Localização:' $shortcutPath -ForegroundColor Cyan; Write-Host 'Executável:' $exePath -ForegroundColor Cyan"

if exist "%SHORTCUT%" (
    echo.
    echo ✅ Atalho atualizado com sucesso!
    echo    Localização: %SHORTCUT%
    echo    Executável: %EXE_PATH%
    echo.
    echo 🎉 Agora o atalho do desktop aponta para a versão mais recente!
) else (
    echo ❌ Erro ao atualizar atalho.
)

echo.
pause

