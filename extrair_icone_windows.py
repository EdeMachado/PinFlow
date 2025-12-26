"""
Tenta extrair o ícone do push pin do Windows
"""

import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
import os

def extract_windows_pin_icon():
    """Tenta extrair ícone do push pin do Windows"""
    app = QApplication(sys.argv)
    
    # Caminhos comuns de DLLs do Windows com ícones
    dll_paths = [
        r"C:\Windows\System32\shell32.dll",
        r"C:\Windows\System32\imageres.dll",
        r"C:\Windows\System32\pifmgr.dll"
    ]
    
    # Índices comuns do push pin no shell32.dll
    # Push pin geralmente está no índice 47 ou 48
    pin_indices = [47, 48, 49, 50, 51, 52, 53, 54, 55]
    
    for dll_path in dll_paths:
        if os.path.exists(dll_path):
            print(f"Verificando {dll_path}...")
            try:
                icon = QIcon(dll_path)
                if not icon.isNull():
                    for idx in pin_indices:
                        # Tentar extrair ícone específico
                        pixmap = icon.pixmap(256, 256)
                        if not pixmap.isNull():
                            filename = f"alfinete_windows_{os.path.basename(dll_path)}_{idx}.png"
                            pixmap.save(filename, 'PNG')
                            print(f"[OK] Ícone extraído: {filename}")
                            return filename
            except Exception as e:
                print(f"Erro ao extrair de {dll_path}: {e}")
    
    print("[AVISO] Não foi possível extrair ícone do Windows")
    print("Criando ícone customizado baseado no design do Windows...")
    return None

if __name__ == '__main__':
    extract_windows_pin_icon()

