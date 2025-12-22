"""
Navegação por Teclado - PinFlow Pro
Implementa navegação completa com Tab, Enter e Setas
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

class KeyboardNavigation:
    """Mixin para navegação por teclado"""
    
    @staticmethod
    def setup_focus_policy(widget):
        """Configura política de foco para widget"""
        widget.setFocusPolicy(Qt.StrongFocus)
        widget.setAttribute(Qt.WA_KeyboardFocusChange, True)
    
    @staticmethod
    def get_focus_style():
        """Retorna estilo CSS para foco visual"""
        return """
            border: 3px solid #2196F3 !important;
            background-color: rgba(33, 150, 243, 0.1) !important;
            outline: 2px solid rgba(33, 150, 243, 0.3) !important;
        """

