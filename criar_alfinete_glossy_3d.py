"""
Cria ícone do alfinete vermelho glossy com perspectiva 3D
"""

from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QLinearGradient, QRadialGradient, QConicalGradient
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPolygon
import sys
import os
import math

def create_glossy_3d_pin():
    """Cria ícone do alfinete vermelho glossy 3D"""
    app = QApplication(sys.argv)
    
    # Criar pixmap 256x256 (alta resolução)
    size = 256
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)  # Fundo transparente
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.TextAntialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)
    
    # === SOMBRA SUAVE ===
    shadow_ellipse = QRect(90, 200, 76, 24)
    shadow_gradient = QLinearGradient(shadow_ellipse.topLeft(), shadow_ellipse.bottomLeft())
    shadow_gradient.setColorAt(0, QColor(0, 0, 0, 35))
    shadow_gradient.setColorAt(0.5, QColor(0, 0, 0, 15))
    shadow_gradient.setColorAt(1, QColor(0, 0, 0, 0))
    painter.setBrush(shadow_gradient)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(shadow_ellipse)
    
    # === PIN METÁLICO (PRATA) ===
    # Corpo do pin - fino e metálico
    pin_body = QRect(120, 150, 8, 50)
    
    # Gradiente metálico prata
    pin_gradient = QLinearGradient(pin_body.left(), pin_body.top(), pin_body.right(), pin_body.top())
    pin_gradient.setColorAt(0, QColor(180, 180, 180))  # Cinza
    pin_gradient.setColorAt(0.3, QColor(240, 240, 240))  # Prata claro
    pin_gradient.setColorAt(0.5, QColor(255, 255, 255))  # Branco (brilho)
    pin_gradient.setColorAt(0.7, QColor(240, 240, 240))  # Prata claro
    pin_gradient.setColorAt(1, QColor(160, 160, 160))  # Cinza escuro
    
    painter.setBrush(pin_gradient)
    painter.setPen(QPen(QColor(130, 130, 130), 1))
    painter.drawRoundedRect(pin_body, 1, 1)
    
    # Linha de brilho no pin
    painter.setPen(QPen(QColor(255, 255, 255, 150), 1))
    painter.drawLine(122, 152, 122, 198)
    
    # Ponta do pin (afiada)
    pin_tip = QPolygon([
        QPoint(120, 200),
        QPoint(128, 200),
        QPoint(124, 210)
    ])
    painter.setBrush(QColor(120, 120, 120))
    painter.setPen(QPen(QColor(100, 100, 100), 1))
    painter.drawPolygon(pin_tip)
    
    # === CABEÇA DO ALFINETE (CILÍNDRICA COM TOPO DOMED) ===
    # Base cilíndrica (parte inferior mais larga)
    base_center_x = 128
    base_center_y = 100
    base_width = 70
    base_height = 25
    
    base_rect = QRect(base_center_x - base_width//2, base_center_y - base_height//2, 
                      base_width, base_height)
    
    # Gradiente para base cilíndrica (vermelho)
    base_gradient = QLinearGradient(base_rect.left(), base_rect.top(), base_rect.right(), base_rect.top())
    base_gradient.setColorAt(0, QColor(200, 0, 0))  # Vermelho escuro (sombra esquerda)
    base_gradient.setColorAt(0.3, QColor(240, 20, 20))  # Vermelho médio
    base_gradient.setColorAt(0.5, QColor(255, 40, 40))  # Vermelho claro (centro)
    base_gradient.setColorAt(0.7, QColor(240, 20, 20))  # Vermelho médio
    base_gradient.setColorAt(1, QColor(180, 0, 0))  # Vermelho escuro (sombra direita)
    
    painter.setBrush(base_gradient)
    painter.setPen(QPen(QColor(160, 0, 0), 1))
    painter.drawRoundedRect(base_rect, 12, 12)
    
    # Topo domed (parte superior arredondada)
    dome_center_x = 128
    dome_center_y = 75
    dome_radius = 35
    
    dome_rect = QRect(dome_center_x - dome_radius, dome_center_y - dome_radius, 
                      dome_radius * 2, dome_radius * 2)
    
    # Gradiente radial para topo domed (vermelho glossy)
    dome_gradient = QRadialGradient(dome_center_x, dome_center_y, dome_radius)
    dome_gradient.setColorAt(0, QColor(255, 80, 80))  # Vermelho muito claro (centro/brilho)
    dome_gradient.setColorAt(0.2, QColor(255, 50, 50))  # Vermelho claro
    dome_gradient.setColorAt(0.4, QColor(240, 30, 30))  # Vermelho médio
    dome_gradient.setColorAt(0.7, QColor(220, 15, 15))  # Vermelho
    dome_gradient.setColorAt(1, QColor(200, 0, 0))  # Vermelho escuro (borda)
    
    painter.setBrush(dome_gradient)
    painter.setPen(QPen(QColor(180, 0, 0), 1.5))
    painter.drawEllipse(dome_rect)
    
    # === BRILHOS E REFLEXOS GLOSSY ===
    # Brilho principal no topo (especular highlight)
    highlight1 = QRect(dome_center_x - 20, dome_center_y - 20, 18, 18)
    highlight_gradient1 = QRadialGradient(highlight1.center().x(), highlight1.center().y(), 9)
    highlight_gradient1.setColorAt(0, QColor(255, 255, 255, 250))  # Branco quase opaco
    highlight_gradient1.setColorAt(0.5, QColor(255, 200, 200, 100))  # Vermelho claro transparente
    highlight_gradient1.setColorAt(1, QColor(255, 200, 200, 0))  # Transparente
    painter.setBrush(highlight_gradient1)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(highlight1)
    
    # Brilho secundário menor (mais intenso)
    highlight2 = QRect(dome_center_x - 12, dome_center_y - 12, 10, 10)
    highlight_gradient2 = QRadialGradient(highlight2.center().x(), highlight2.center().y(), 5)
    highlight_gradient2.setColorAt(0, QColor(255, 255, 255, 255))  # Branco total
    highlight_gradient2.setColorAt(1, QColor(255, 255, 255, 0))  # Transparente
    painter.setBrush(highlight_gradient2)
    painter.drawEllipse(highlight2)
    
    # Reflexo na lateral direita (curvatura)
    highlight3 = QRect(dome_center_x + 15, dome_center_y - 5, 20, 30)
    highlight_gradient3 = QLinearGradient(highlight3.left(), highlight3.top(), highlight3.right(), highlight3.top())
    highlight_gradient3.setColorAt(0, QColor(255, 150, 150, 120))  # Vermelho claro transparente
    highlight_gradient3.setColorAt(1, QColor(255, 150, 150, 0))  # Transparente
    painter.setBrush(highlight_gradient3)
    painter.drawEllipse(highlight3)
    
    # Borda sutil
    painter.setBrush(Qt.NoBrush)
    painter.setPen(QPen(QColor(150, 0, 0), 1))
    painter.drawEllipse(dome_rect)
    
    painter.end()
    
    # Salvar
    pixmap.save('alfinete_vermelho.png', 'PNG')
    print("[OK] alfinete_vermelho.png criado (glossy 3D)!")
    
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
    create_glossy_3d_pin()

