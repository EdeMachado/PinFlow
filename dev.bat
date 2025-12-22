@echo off
REM Script de desenvolvimento - recarrega automaticamente ao fazer alterações

echo ========================================
echo    Post-it Kanban Pro - DEV MODE
echo ========================================
echo.
echo Modo desenvolvimento ativo!
echo O programa sera reiniciado ao salvar main.py
echo.
echo Pressione Ctrl+C para sair
echo.

pip install -q watchdog

python -c "
import time
import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_app()
        
    def start_app(self):
        if self.process:
            self.process.terminate()
            time.sleep(0.5)
        print('\n[RELOAD] Iniciando aplicacao...\n')
        self.process = subprocess.Popen([sys.executable, 'main.py'])
        
    def on_modified(self, event):
        if event.src_path.endswith('main.py'):
            print(f'\n[CHANGE] Detectada alteracao em {event.src_path}')
            time.sleep(0.5)
            self.start_app()

handler = ChangeHandler()
observer = Observer()
observer.schedule(handler, '.', recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    if handler.process:
        handler.process.terminate()
    print('\n\n[EXIT] Dev mode encerrado')
    
observer.join()
"




