"""
Cria ícone do alfinete vermelho para PinFlow Pro
"""

from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QLinearGradient
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPolygon
import sys
import os

def create_red_pin_icon():
    """Cria ícone do alfinete vermelho"""
    app = QApplication(sys.argv)
    
    # Criar pixmap 256x256 (alta resolução)
    size = 256
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)  # Fundo transparente
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.TextAntialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)
    
    # === SOMBRA DO ALFINETE ===
    shadow_ellipse = QRect(100, 200, 56, 20)
    shadow_gradient = QLinearGradient(shadow_ellipse.topLeft(), shadow_ellipse.bottomLeft())
    shadow_gradient.setColorAt(0, QColor(0, 0, 0, 30))
    shadow_gradient.setColorAt(1, QColor(0, 0, 0, 0))
    painter.setBrush(shadow_gradient)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(shadow_ellipse)
    
    # === CORPO DO PIN (METÁLICO) ===
    # Corpo principal (cilindro)
    pin_body = QRect(118, 140, 20, 60)
    pin_gradient = QLinearGradient(pin_body.left(), pin_body.top(), pin_body.right(), pin_body.top())
    pin_gradient.setColorAt(0, QColor(180, 180, 180))  # Cinza escuro (sombra)
    pin_gradient.setColorAt(0.5, QColor(240, 240, 240))  # Cinza claro (brilho)
    pin_gradient.setColorAt(1, QColor(200, 200, 200))  # Cinza médio
    painter.setBrush(pin_gradient)
    painter.setPen(QPen(QColor(160, 160, 160), 1))
    painter.drawRoundedRect(pin_body, 10, 10)
    
    # Brilho no pin (linha de luz)
    painter.setPen(QPen(QColor(255, 255, 255, 150), 2))
    painter.drawLine(123, 145, 123, 195)
    
    # Ponta do pin (mais escura)
    pin_tip = QPolygon([
        QPoint(118, 200),
        QPoint(138, 200),
        QPoint(128, 210)
    ])
    painter.setBrush(QColor(140, 140, 140))
    painter.setPen(Qt.NoPen)
    painter.drawPolygon(pin_tip)
    
    # === CABEÇA DO ALFINETE (VERMELHO BRILHANTE) ===
    head_rect = QRect(78, 50, 100, 100)
    
    # Gradiente radial para efeito 3D esférico (VERMELHO)
    head_gradient = QLinearGradient(head_rect.topLeft(), head_rect.bottomRight())
    head_gradient.setColorAt(0, QColor(255, 60, 60))  # Vermelho claro (brilho superior esquerdo)
    head_gradient.setColorAt(0.3, QColor(220, 20, 20))  # Vermelho médio
    head_gradient.setColorAt(0.7, QColor(180, 0, 0))  # Vermelho escuro
    head_gradient.setColorAt(1, QColor(150, 0, 0))  # Vermelho muito escuro (sombra inferior direita)
    
    painter.setBrush(head_gradient)
    painter.setPen(QPen(QColor(200, 0, 0), 2))
    painter.drawEllipse(head_rect)
    
    # === BRILHO PRINCIPAL (HIGHLIGHT) ===
    # Brilho grande no canto superior esquerdo
    highlight1 = QRect(88, 60, 50, 50)
    highlight_gradient1 = QLinearGradient(highlight1.topLeft(), highlight1.bottomRight())
    highlight_gradient1.setColorAt(0, QColor(255, 200, 200, 200))  # Branco semi-transparente
    highlight_gradient1.setColorAt(1, QColor(255, 200, 200, 0))  # Transparente
    painter.setBrush(highlight_gradient1)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(highlight1)
    
    # Brilho secundário (menor, mais intenso)
    highlight2 = QRect(95, 68, 25, 25)
    highlight_gradient2 = QLinearGradient(highlight2.topLeft(), highlight2.bottomRight())
    highlight_gradient2.setColorAt(0, QColor(255, 255, 255, 180))
    highlight_gradient2.setColorAt(1, QColor(255, 255, 255, 0))
    painter.setBrush(highlight_gradient2)
    painter.drawEllipse(highlight2)
    
    # Brilho alongado na lateral direita
    highlight3 = QRect(140, 70, 30, 50)
    highlight_gradient3 = QLinearGradient(highlight3.left(), highlight3.top(), highlight3.right(), highlight3.top())
    highlight_gradient3.setColorAt(0, QColor(255, 150, 150, 120))
    highlight_gradient3.setColorAt(1, QColor(255, 150, 150, 0))
    painter.setBrush(highlight_gradient3)
    painter.drawEllipse(highlight3)
    
    # Borda sutil para definição
    painter.setBrush(Qt.NoBrush)
    painter.setPen(QPen(QColor(180, 0, 0), 1))
    painter.drawEllipse(head_rect)
    
    painter.end()
    
    # Salvar como PNG
    pixmap.save('alfinete_vermelho.png', 'PNG')
    print("[OK] alfinete_vermelho.png criado!")
    
    # Salvar diferentes tamanhos
    sizes = [16, 24, 32, 48, 64, 128, 256]
    for ico_size in sizes:
        scaled = pixmap.scaled(ico_size, ico_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        scaled.save(f'alfinete_vermelho_{ico_size}.png', 'PNG')
    
    # Tentar criar .ico usando PIL se disponível
    try:
        from PIL import Image
        img = Image.open('alfinete_vermelho.png')
        img.save('alfinete_vermelho.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
        print("[OK] alfinete_vermelho.ico criado!")
    except ImportError:
        print("[AVISO] PIL não instalado. Use um conversor online para criar o .ico")
        print("   https://convertio.co/pt/png-ico/")
    
    app.quit()

if __name__ == '__main__':
    create_red_pin_icon()

