@echo off
chcp 65001 > nul
echo ═══════════════════════════════════════════════════════════════
echo 📦 CRIAR INSTALADOR - Post-it Kanban Pro
echo ═══════════════════════════════════════════════════════════════
echo.

echo [1/4] Instalando PyInstaller...
pip install pyinstaller
echo.

echo [2/4] Criando executável...
echo Isso pode levar alguns minutos...
pyinstaller --onefile --windowed --name "PostitKanbanPro" --icon=icon.ico main.py 2>nul
if not exist "dist\PostitKanbanPro.exe" (
    echo ❌ Erro ao criar executável
    echo Tentando sem ícone...
    pyinstaller --onefile --windowed --name "PostitKanbanPro" main.py
)
echo.

echo [3/4] Limpando arquivos temporários...
if exist "build" rmdir /s /q build
if exist "PostitKanbanPro.spec" del /q PostitKanbanPro.spec
echo.

echo [4/4] Verificando resultado...
if exist "dist\PostitKanbanPro.exe" (
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo ✅ SUCESSO! Executável criado com sucesso!
    echo ═══════════════════════════════════════════════════════════════
    echo.
    echo 📂 Localização: dist\PostitKanbanPro.exe
    echo 📏 Tamanho: 
    dir "dist\PostitKanbanPro.exe" | find "PostitKanbanPro.exe"
    echo.
    echo 📋 PRÓXIMOS PASSOS:
    echo 1. Teste o executável em outra máquina (sem Python)
    echo 2. Se funcionar, está pronto para distribuir!
    echo 3. Opcional: Use Inno Setup para criar instalador .exe
    echo.
    echo 💡 DICA: Comprima o executável em um .zip para distribuir
    echo.
    
    explorer "dist"
) else (
    echo ❌ ERRO: Executável não foi criado
    echo Verifique se o arquivo main.py existe
    pause
)

pause




