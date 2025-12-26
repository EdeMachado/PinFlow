"""
Cria ícone do alfinete EXATAMENTE como o do Windows
"""

from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QLinearGradient, QRadialGradient
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPolygon
import sys
import os

def create_exact_windows_pin():
    """Cria ícone do alfinete exatamente como o Windows"""
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
    shadow_ellipse = QRect(98, 198, 60, 20)
    shadow_gradient = QLinearGradient(shadow_ellipse.topLeft(), shadow_ellipse.bottomLeft())
    shadow_gradient.setColorAt(0, QColor(0, 0, 0, 25))
    shadow_gradient.setColorAt(1, QColor(0, 0, 0, 0))
    painter.setBrush(shadow_gradient)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(shadow_ellipse)
    
    # === PIN (METÁLICO RETO E SIMPLES) ===
    # Corpo do pin - retângulo fino e reto
    pin_body = QRect(122, 160, 12, 40)
    
    # Gradiente metálico simples
    pin_gradient = QLinearGradient(pin_body.left(), pin_body.top(), pin_body.right(), pin_body.top())
    pin_gradient.setColorAt(0, QColor(190, 190, 190))  # Cinza claro
    pin_gradient.setColorAt(0.5, QColor(230, 230, 230))  # Prata claro
    pin_gradient.setColorAt(1, QColor(170, 170, 170))  # Cinza médio
    
    painter.setBrush(pin_gradient)
    painter.setPen(QPen(QColor(140, 140, 140), 1))
    painter.drawRoundedRect(pin_body, 1, 1)
    
    # Linha de brilho sutil no pin
    painter.setPen(QPen(QColor(255, 255, 255, 120), 1))
    painter.drawLine(124, 162, 124, 198)
    
    # Ponta do pin (triângulo pequeno e afiado)
    pin_tip = QPolygon([
        QPoint(122, 200),
        QPoint(134, 200),
        QPoint(128, 208)
    ])
    painter.setBrush(QColor(130, 130, 130))
    painter.setPen(QPen(QColor(110, 110, 110), 1))
    painter.drawPolygon(pin_tip)
    
    # === CABEÇA DO ALFINETE (CÍRCULO VERMELHO PERFEITO) ===
    # Círculo vermelho estilo Windows - PERFEITAMENTE REDONDO
    head_center_x = 128
    head_center_y = 90
    head_radius = 50  # Raio maior para cabeça mais visível
    
    head_rect = QRect(head_center_x - head_radius, head_center_y - head_radius, 
                      head_radius * 2, head_radius * 2)
    
    # Gradiente radial (vermelho sólido estilo Windows)
    head_gradient = QRadialGradient(head_center_x, head_center_y, head_radius)
    head_gradient.setColorAt(0, QColor(255, 80, 80))  # Vermelho claro (centro)
    head_gradient.setColorAt(0.25, QColor(240, 40, 40))  # Vermelho médio-claro
    head_gradient.setColorAt(0.5, QColor(220, 20, 20))  # Vermelho médio
    head_gradient.setColorAt(0.75, QColor(200, 0, 0))  # Vermelho
    head_gradient.setColorAt(1, QColor(180, 0, 0))  # Vermelho escuro (borda)
    
    painter.setBrush(head_gradient)
    painter.setPen(QPen(QColor(150, 0, 0), 2))
    painter.drawEllipse(head_rect)  # Círculo PERFEITO
    
    # === BRILHO ESTILO WINDOWS (PEQUENO E SUTIL) ===
    # Brilho no canto superior esquerdo (bem pequeno)
    highlight_x = head_center_x - 20
    highlight_y = head_center_y - 20
    highlight_size = 18
    
    highlight = QRect(highlight_x, highlight_y, highlight_size, highlight_size)
    highlight_gradient = QRadialGradient(highlight.center().x(), highlight.center().y(), highlight_size/2)
    highlight_gradient.setColorAt(0, QColor(255, 255, 255, 220))  # Branco
    highlight_gradient.setColorAt(0.6, QColor(255, 200, 200, 80))  # Vermelho claro transparente
    highlight_gradient.setColorAt(1, QColor(255, 200, 200, 0))  # Transparente
    painter.setBrush(highlight_gradient)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(highlight)
    
    # Borda externa sutil
    painter.setBrush(Qt.NoBrush)
    painter.setPen(QPen(QColor(130, 0, 0), 1))
    painter.drawEllipse(head_rect)
    
    painter.end()
    
    # Salvar como PNG primeiro
    pixmap.save('alfinete_vermelho.png', 'PNG')
    print("[OK] alfinete_vermelho.png criado (estilo Windows exato)!")
    
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
    create_exact_windows_pin()

