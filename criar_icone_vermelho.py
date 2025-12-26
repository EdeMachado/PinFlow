"""
Cria ícone vermelho do alfinete para PinFlow Pro
"""

from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QLinearGradient
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPolygon
import sys
import os

def create_red_icon():
    """Cria ícone vermelho do alfinete"""
    app = QApplication(sys.argv)
    
    # Criar pixmap 256x256 (alta resolução)
    size = 256
    pixmap = QPixmap(size, size)
    pixmap.fill(QColor(255, 255, 255, 0))  # Fundo transparente
    
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
    
    # Gradiente radial para efeito 3D esférico - VERMELHO
    head_gradient = QLinearGradient(head_rect.topLeft(), head_rect.bottomRight())
    head_gradient.setColorAt(0, QColor(255, 100, 100))  # Vermelho claro (brilho superior esquerdo)
    head_gradient.setColorAt(0.3, QColor(220, 40, 40))  # Vermelho médio
    head_gradient.setColorAt(0.7, QColor(200, 20, 20))  # Vermelho escuro
    head_gradient.setColorAt(1, QColor(180, 10, 10))  # Vermelho muito escuro (sombra inferior direita)
    
    painter.setBrush(head_gradient)
    painter.setPen(QPen(QColor(200, 20, 20), 2))
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
    highlight_gradient3.setColorAt(0, QColor(255, 180, 180, 120))
    highlight_gradient3.setColorAt(1, QColor(255, 180, 180, 0))
    painter.setBrush(highlight_gradient3)
    painter.drawEllipse(highlight3)
    
    # Borda sutil para definição
    painter.setBrush(Qt.NoBrush)
    painter.setPen(QPen(QColor(180, 20, 20), 1))
    painter.drawEllipse(head_rect)
    
    painter.end()
    
    # Salvar como PNG primeiro
    pixmap.save('alfinete_vermelho.png', 'PNG')
    print("[OK] PNG criado: alfinete_vermelho.png")
    
    # Tentar criar .ico usando o PNG
    # Para .ico completo, seria necessário usar biblioteca externa ou converter online
    # Por enquanto, vamos copiar o PNG e renomear (Windows aceita PNG como ícone em alguns casos)
    # Ou usar o ícone verde existente como base e modificar
    
    # Se existe alfinete_verde.ico, vamos tentar usá-lo como base
    if os.path.exists("alfinete_verde.ico"):
        print("[INFO] Usando alfinete_verde.ico como base...")
        # Copiar e renomear (será substituído por conversão adequada depois)
        import shutil
        shutil.copy("alfinete_verde.ico", "alfinete_vermelho.ico")
        print("[OK] Ícone temporário criado: alfinete_vermelho.ico")
        print("[AVISO] Para melhor resultado, converta alfinete_vermelho.png para .ico usando:")
        print("   - https://convertio.co/pt/png-ico/")
        print("   - Ou ImageMagick: magick convert alfinete_vermelho.png alfinete_vermelho.ico")
    else:
        # Criar ícone básico do PNG
        icon = QIcon(pixmap)
        # Salvar como .ico (Qt pode fazer isso)
        icon_file = "alfinete_vermelho.ico"
        # Infelizmente Qt não salva .ico diretamente, então vamos criar um PNG e depois converter
        print("[INFO] PNG criado. Para criar .ico, use um conversor online ou ImageMagick")
    
    print("\n[SUCESSO] Ícone vermelho criado!")
    print("  - alfinete_vermelho.png")
    if os.path.exists("alfinete_vermelho.ico"):
        print("  - alfinete_vermelho.ico")
    
    app.quit()

if __name__ == '__main__':
    create_red_icon()

