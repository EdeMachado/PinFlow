"""
Cria ícone do alfinete vermelho melhorado para PinFlow Pro
"""

from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QLinearGradient, QRadialGradient
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPolygon
import sys
import os

def create_red_pin_icon():
    """Cria ícone do alfinete vermelho melhorado"""
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
    shadow_gradient.setColorAt(0, QColor(0, 0, 0, 40))
    shadow_gradient.setColorAt(1, QColor(0, 0, 0, 0))
    painter.setBrush(shadow_gradient)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(shadow_ellipse)
    
    # === CORPO DO PIN (METÁLICO CROMADO) ===
    pin_body = QRect(118, 140, 20, 60)
    
    # Gradiente metálico mais realista
    pin_gradient = QLinearGradient(pin_body.left(), pin_body.top(), pin_body.right(), pin_body.top())
    pin_gradient.setColorAt(0, QColor(160, 160, 160))  # Cinza escuro (sombra esquerda)
    pin_gradient.setColorAt(0.3, QColor(240, 240, 240))  # Prata claro (brilho)
    pin_gradient.setColorAt(0.5, QColor(255, 255, 255))  # Branco (reflexo máximo)
    pin_gradient.setColorAt(0.7, QColor(240, 240, 240))  # Prata claro
    pin_gradient.setColorAt(1, QColor(180, 180, 180))  # Cinza médio (sombra direita)
    
    painter.setBrush(pin_gradient)
    painter.setPen(QPen(QColor(140, 140, 140), 1))
    painter.drawRoundedRect(pin_body, 10, 10)
    
    # Brilho no pin (linha de luz vertical)
    painter.setPen(QPen(QColor(255, 255, 255, 180), 2))
    painter.drawLine(123, 145, 123, 195)
    
    # Ponta do pin (mais escura, afiada)
    pin_tip = QPolygon([
        QPoint(118, 200),
        QPoint(138, 200),
        QPoint(128, 215)
    ])
    painter.setBrush(QColor(120, 120, 120))
    painter.setPen(QPen(QColor(100, 100, 100), 1))
    painter.drawPolygon(pin_tip)
    
    # === CABEÇA DO ALFINETE (VERMELHO VIVO E BRILHANTE) ===
    head_rect = QRect(78, 50, 100, 100)
    
    # Gradiente radial para efeito 3D esférico (VERMELHO VIVO)
    head_gradient = QRadialGradient(head_rect.center(), head_rect.width()/2)
    head_gradient.setColorAt(0, QColor(255, 80, 80))  # Vermelho muito claro (brilho central)
    head_gradient.setColorAt(0.2, QColor(255, 40, 40))  # Vermelho claro
    head_gradient.setColorAt(0.4, QColor(220, 20, 20))  # Vermelho médio
    head_gradient.setColorAt(0.7, QColor(180, 0, 0))  # Vermelho escuro
    head_gradient.setColorAt(1, QColor(140, 0, 0))  # Vermelho muito escuro (borda)
    
    painter.setBrush(head_gradient)
    painter.setPen(QPen(QColor(160, 0, 0), 2))
    painter.drawEllipse(head_rect)
    
    # === BRILHO PRINCIPAL (HIGHLIGHT BRANCO) ===
    # Brilho grande no canto superior esquerdo
    highlight1 = QRect(88, 60, 45, 45)
    highlight_gradient1 = QRadialGradient(highlight1.center(), highlight1.width()/2)
    highlight_gradient1.setColorAt(0, QColor(255, 255, 255, 220))  # Branco quase opaco
    highlight_gradient1.setColorAt(0.5, QColor(255, 200, 200, 100))  # Vermelho claro transparente
    highlight_gradient1.setColorAt(1, QColor(255, 200, 200, 0))  # Transparente
    painter.setBrush(highlight_gradient1)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(highlight1)
    
    # Brilho secundário (menor, mais intenso)
    highlight2 = QRect(95, 68, 20, 20)
    highlight_gradient2 = QRadialGradient(highlight2.center(), highlight2.width()/2)
    highlight_gradient2.setColorAt(0, QColor(255, 255, 255, 255))  # Branco total
    highlight_gradient2.setColorAt(1, QColor(255, 255, 255, 0))  # Transparente
    painter.setBrush(highlight_gradient2)
    painter.drawEllipse(highlight2)
    
    # Brilho alongado na lateral direita (reflexo)
    highlight3 = QRect(140, 75, 25, 40)
    highlight_gradient3 = QLinearGradient(highlight3.left(), highlight3.top(), highlight3.right(), highlight3.top())
    highlight_gradient3.setColorAt(0, QColor(255, 150, 150, 150))
    highlight_gradient3.setColorAt(1, QColor(255, 150, 150, 0))
    painter.setBrush(highlight_gradient3)
    painter.drawEllipse(highlight3)
    
    # Borda sutil para definição
    painter.setBrush(Qt.NoBrush)
    painter.setPen(QPen(QColor(120, 0, 0), 1.5))
    painter.drawEllipse(head_rect)
    
    painter.end()
    
    # Salvar como PNG
    pixmap.save('alfinete_vermelho.ico', 'PNG')
    print("[OK] alfinete_vermelho.ico criado!")
    
    # Tentar criar .ico usando PIL se disponível
    try:
        from PIL import Image
        img = Image.open('alfinete_vermelho.ico')
        # Converter para ICO com múltiplos tamanhos
        ico_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
        img.save('alfinete_vermelho.ico', format='ICO', sizes=ico_sizes)
        print("[OK] alfinete_vermelho.ico criado com múltiplos tamanhos!")
    except ImportError:
        print("[AVISO] PIL não instalado. PNG criado, converta para ICO manualmente")
    except Exception as e:
        print(f"[AVISO] Erro ao criar ICO: {e}")
        print("PNG criado, converta para ICO manualmente")
    
    app.quit()

if __name__ == '__main__':
    create_red_pin_icon()

