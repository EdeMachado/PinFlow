"""
Cria ícone do alfinete no estilo Windows (push pin)
"""

from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QLinearGradient, QRadialGradient
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPolygon
import sys
import os

def create_windows_style_pin():
    """Cria ícone do alfinete no estilo Windows"""
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
    shadow_ellipse = QRect(100, 200, 56, 18)
    shadow_gradient = QLinearGradient(shadow_ellipse.topLeft(), shadow_ellipse.bottomLeft())
    shadow_gradient.setColorAt(0, QColor(0, 0, 0, 30))
    shadow_gradient.setColorAt(1, QColor(0, 0, 0, 0))
    painter.setBrush(shadow_gradient)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(shadow_ellipse)
    
    # === PIN (METÁLICO SIMPLES) ===
    # Corpo do pin - retângulo simples
    pin_body = QRect(120, 150, 16, 50)
    pin_gradient = QLinearGradient(pin_body.left(), pin_body.top(), pin_body.right(), pin_body.top())
    pin_gradient.setColorAt(0, QColor(200, 200, 200))  # Cinza claro
    pin_gradient.setColorAt(0.5, QColor(240, 240, 240))  # Prata
    pin_gradient.setColorAt(1, QColor(180, 180, 180))  # Cinza médio
    painter.setBrush(pin_gradient)
    painter.setPen(QPen(QColor(150, 150, 150), 1))
    painter.drawRoundedRect(pin_body, 2, 2)
    
    # Linha de brilho no pin
    painter.setPen(QPen(QColor(255, 255, 255, 150), 1.5))
    painter.drawLine(122, 152, 122, 198)
    
    # Ponta do pin (triângulo afiado)
    pin_tip = QPolygon([
        QPoint(120, 200),
        QPoint(136, 200),
        QPoint(128, 210)
    ])
    painter.setBrush(QColor(140, 140, 140))
    painter.setPen(QPen(QColor(120, 120, 120), 1))
    painter.drawPolygon(pin_tip)
    
    # === CABEÇA DO ALFINETE (CÍRCULO VERMELHO SIMPLES) ===
    # Círculo vermelho estilo Windows
    head_center_x = 128
    head_center_y = 100
    head_radius = 45
    
    head_rect = QRect(head_center_x - head_radius, head_center_y - head_radius, 
                      head_radius * 2, head_radius * 2)
    
    # Gradiente radial simples (vermelho sólido com brilho)
    head_gradient = QRadialGradient(head_center_x, head_center_y, head_radius)
    head_gradient.setColorAt(0, QColor(255, 60, 60))  # Vermelho claro (centro)
    head_gradient.setColorAt(0.3, QColor(220, 20, 20))  # Vermelho médio
    head_gradient.setColorAt(0.6, QColor(200, 0, 0))  # Vermelho
    head_gradient.setColorAt(1, QColor(180, 0, 0))  # Vermelho escuro (borda)
    
    painter.setBrush(head_gradient)
    painter.setPen(QPen(QColor(160, 0, 0), 2))
    painter.drawEllipse(head_rect)
    
    # === BRILHO SIMPLES (ESTILO WINDOWS) ===
    # Brilho no canto superior esquerdo (pequeno e sutil)
    highlight = QRect(head_center_x - 25, head_center_y - 25, 20, 20)
    highlight_gradient = QRadialGradient(highlight.center().x(), highlight.center().y(), 10)
    highlight_gradient.setColorAt(0, QColor(255, 255, 255, 200))  # Branco
    highlight_gradient.setColorAt(1, QColor(255, 255, 255, 0))  # Transparente
    painter.setBrush(highlight_gradient)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(highlight)
    
    # Borda externa sutil
    painter.setBrush(Qt.NoBrush)
    painter.setPen(QPen(QColor(140, 0, 0), 1))
    painter.drawEllipse(head_rect)
    
    painter.end()
    
    # Salvar como PNG primeiro
    pixmap.save('alfinete_vermelho.png', 'PNG')
    print("[OK] alfinete_vermelho.png criado (estilo Windows)!")
    
    # Tentar criar .ico usando PIL
    try:
        from PIL import Image
        img = Image.open('alfinete_vermelho.png')
        # Criar ICO com múltiplos tamanhos
        ico_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
        img.save('alfinete_vermelho.ico', format='ICO', sizes=ico_sizes)
        print("[OK] alfinete_vermelho.ico criado com múltiplos tamanhos!")
    except ImportError:
        print("[AVISO] PIL não instalado. PNG criado, converta para ICO")
    except Exception as e:
        print(f"[AVISO] Erro ao criar ICO: {e}")
        print("PNG criado, converta para ICO manualmente")
    
    app.quit()

if __name__ == '__main__':
    create_windows_style_pin()

