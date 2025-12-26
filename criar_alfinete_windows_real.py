"""
Cria ícone do alfinete como o REAL do Windows (cabeça achatada/oval)
"""

from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QLinearGradient, QRadialGradient
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPolygon
import sys
import os

def create_real_windows_pin():
    """Cria ícone do alfinete como o real do Windows"""
    app = QApplication(sys.argv)
    
    # Criar pixmap 256x256 (alta resolução)
    size = 256
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)  # Fundo transparente
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.TextAntialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)
    
    # === SOMBRA ===
    shadow_ellipse = QRect(95, 195, 66, 22)
    shadow_gradient = QLinearGradient(shadow_ellipse.topLeft(), shadow_ellipse.bottomLeft())
    shadow_gradient.setColorAt(0, QColor(0, 0, 0, 30))
    shadow_gradient.setColorAt(1, QColor(0, 0, 0, 0))
    painter.setBrush(shadow_gradient)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(shadow_ellipse)
    
    # === PIN (METÁLICO FINO) ===
    pin_body = QRect(123, 155, 10, 45)
    
    # Gradiente metálico
    pin_gradient = QLinearGradient(pin_body.left(), pin_body.top(), pin_body.right(), pin_body.top())
    pin_gradient.setColorAt(0, QColor(185, 185, 185))
    pin_gradient.setColorAt(0.5, QColor(235, 235, 235))
    pin_gradient.setColorAt(1, QColor(165, 165, 165))
    
    painter.setBrush(pin_gradient)
    painter.setPen(QPen(QColor(135, 135, 135), 1))
    painter.drawRoundedRect(pin_body, 1, 1)
    
    # Linha de brilho
    painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
    painter.drawLine(125, 157, 125, 198)
    
    # Ponta do pin
    pin_tip = QPolygon([
        QPoint(123, 200),
        QPoint(133, 200),
        QPoint(128, 207)
    ])
    painter.setBrush(QColor(125, 125, 125))
    painter.setPen(QPen(QColor(105, 105, 105), 1))
    painter.drawPolygon(pin_tip)
    
    # === CABEÇA DO ALFINETE (OVAL/ACHATADA - ESTILO WINDOWS REAL) ===
    # Cabeça OVAL (mais larga que alta) - estilo Windows real
    head_center_x = 128
    head_center_y = 85
    head_width = 100  # Largura (horizontal)
    head_height = 75  # Altura (vertical) - menor que largura = oval
    
    head_rect = QRect(head_center_x - head_width//2, head_center_y - head_height//2, 
                      head_width, head_height)
    
    # Gradiente radial (vermelho)
    head_gradient = QRadialGradient(head_center_x, head_center_y, head_width//2)
    head_gradient.setColorAt(0, QColor(255, 70, 70))
    head_gradient.setColorAt(0.3, QColor(235, 35, 35))
    head_gradient.setColorAt(0.6, QColor(215, 15, 15))
    head_gradient.setColorAt(1, QColor(175, 0, 0))
    
    painter.setBrush(head_gradient)
    painter.setPen(QPen(QColor(145, 0, 0), 2))
    painter.drawEllipse(head_rect)  # Oval
    
    # === BRILHO ===
    highlight_x = head_center_x - 18
    highlight_y = head_center_y - 15
    highlight = QRect(highlight_x, highlight_y, 16, 16)
    highlight_gradient = QRadialGradient(highlight.center().x(), highlight.center().y(), 8)
    highlight_gradient.setColorAt(0, QColor(255, 255, 255, 200))
    highlight_gradient.setColorAt(1, QColor(255, 255, 255, 0))
    painter.setBrush(highlight_gradient)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(highlight)
    
    # Borda
    painter.setBrush(Qt.NoBrush)
    painter.setPen(QPen(QColor(125, 0, 0), 1))
    painter.drawEllipse(head_rect)
    
    painter.end()
    
    # Salvar
    pixmap.save('alfinete_vermelho.png', 'PNG')
    print("[OK] alfinete_vermelho.png criado (cabeça oval estilo Windows)!")
    
    try:
        from PIL import Image
        img = Image.open('alfinete_vermelho.png')
        ico_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
        img.save('alfinete_vermelho.ico', format='ICO', sizes=ico_sizes)
        print("[OK] alfinete_vermelho.ico criado!")
    except Exception as e:
        print(f"[AVISO] Erro ao criar ICO: {e}")
    
    app.quit()

if __name__ == '__main__':
    create_real_windows_pin()

