@echo off
echo ========================================
echo LIMPEZA DE CARDS EM BRANCO
echo ========================================
echo.
echo Este script vai remover cards em branco do seu Kanban.
echo.
pause

cd /d "%~dp0"

python -c "import json; data = json.load(open('kanban.json', 'r', encoding='utf-8')); [col.update({'cards': [c for c in col.get('cards', []) if c.get('titulo', '').strip()]}) for col in data.get('columns', [])]; json.dump(data, open('kanban.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False); print('Cards em branco removidos com sucesso!')"

echo.
echo ========================================
echo Pronto! Execute run.bat para ver o resultado.
echo ========================================
pause




