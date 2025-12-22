"""
Cria um ícone profissional para PinFlow Pro
Gera arquivo .ico com múltiplas resoluções
"""

from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QPen, QLinearGradient
from PySide6.QtCore import Qt, QRect
from PySide6.QtWidgets import QApplication
import sys

def create_icon():
    """Cria ícone profissional com logo PinFlow"""
    app = QApplication(sys.argv)
    
    # Criar pixmap 256x256 (alta resolução)
    size = 256
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.TextAntialiasing)
    
    # Fundo com gradiente azul → prata
    gradient = QLinearGradient(0, 0, 0, size)
    gradient.setColorAt(0, QColor(20, 30, 70))  # Azul escuro
    gradient.setColorAt(1, QColor(150, 160, 180))  # Prata
    painter.setBrush(gradient)
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(0, 0, size, size, 30, 30)
    
    # Borda externa
    pen = QPen(QColor(255, 255, 255, 100))
    pen.setWidth(4)
    painter.setPen(pen)
    painter.setBrush(Qt.NoBrush)
    painter.drawRoundedRect(4, 4, size-8, size-8, 28, 28)
    
    # Ícone de Pin (📌)
    painter.setPen(Qt.NoPen)
    # Cabeça do pin
    painter.setBrush(QColor(255, 100, 100))  # Vermelho
    painter.drawEllipse(QRect(75, 50, 40, 40))
    # Corpo do pin
    painter.setBrush(QColor(200, 200, 200))  # Cinza claro
    points = [
        (95, 90),   # Topo
        (110, 180), # Direita
        (95, 200),  # Ponta
        (80, 180),  # Esquerda
    ]
    from PySide6.QtGui import QPolygon
    from PySide6.QtCore import QPoint
    polygon = QPolygon([QPoint(x, y) for x, y in points])
    painter.drawPolygon(polygon)
    
    # Seta (➜)
    painter.setBrush(QColor(100, 255, 100))  # Verde
    pen = QPen(QColor(100, 255, 100))
    pen.setWidth(12)
    painter.setPen(pen)
    # Linha da seta
    painter.drawLine(130, 100, 200, 100)
    # Ponta da seta
    arrow_points = [
        (200, 100),  # Ponta
        (180, 85),   # Superior
        (180, 115),  # Inferior
    ]
    arrow_polygon = QPolygon([QPoint(x, y) for x, y in arrow_points])
    painter.drawPolygon(arrow_polygon)
    
    # Texto "P"
    font = QFont("Arial", 80, QFont.Bold)
    painter.setFont(font)
    painter.setPen(QColor(255, 255, 255))
    painter.drawText(QRect(0, 120, size, 100), Qt.AlignCenter, "P")
    
    painter.end()
    
    # Salvar como .ico com múltiplas resoluções
    icon = QIcon(pixmap)
    
    # Salvar diferentes tamanhos
    for ico_size in [16, 24, 32, 48, 64, 128, 256]:
        scaled = pixmap.scaled(ico_size, ico_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        scaled.save(f'icon_{ico_size}.png', 'PNG')
    
    # Salvar PNG principal
    pixmap.save('icon.png', 'PNG')
    
    print("✓ Ícones criados com sucesso!")
    print("  - icon.png (256x256)")
    print("  - icon_*.png (múltiplos tamanhos)")
    print("")
    print("⚠️  Para criar o .ico, use um conversor online:")
    print("   https://convertio.co/pt/png-ico/")
    print("   Ou use 'magick convert icon.png icon.ico' (ImageMagick)")
    
    app.quit()

if __name__ == '__main__':
    create_icon()

