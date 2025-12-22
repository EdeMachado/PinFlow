@echo off
echo ========================================
echo   REMOVER INICIALIZACAO AUTOMATICA
echo   Post-it Kanban Pro
echo ========================================
echo.

REM Caminho da pasta Startup
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

REM Verificar se o atalho existe
if exist "%STARTUP_FOLDER%\PostitKanban.lnk" (
    echo Removendo atalho...
    del "%STARTUP_FOLDER%\PostitKanban.lnk"
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ========================================
        echo   ATALHO REMOVIDO!
        echo ========================================
        echo.
        echo O Kanban NAO vai mais abrir
        echo automaticamente ao ligar o PC.
        echo.
        echo Voce ainda pode abrir manualmente
        echo executando run.bat
        echo.
    ) else (
        echo [ERRO] Nao foi possivel remover!
    )
) else (
    echo.
    echo [INFO] Atalho nao encontrado!
    echo O Kanban ja nao esta na inicializacao.
    echo.
)

pause




