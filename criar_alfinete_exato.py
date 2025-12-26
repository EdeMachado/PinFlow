"""
Cria ícone do alfinete EXATAMENTE como na imagem
- Cabeça domed (topo arredondado)
- Shaft cilíndrico com indentação
- Base circular mais larga
- Pin metálico prata
- Highlights brancos glossy
"""

from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QLinearGradient, QRadialGradient
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPolygon
import sys
import os

def create_exact_pin():
    """Cria ícone exatamente como na imagem"""
    app = QApplication(sys.argv)
    
    # Criar pixmap 256x256 (alta resolução)
    size = 256
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)  # Fundo transparente
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.TextAntialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)
    
    # === PIN METÁLICO (PRATA) ===
    # Pin fino e afiado
    pin_start_x = 128
    pin_start_y = 200
    pin_end_x = 128
    pin_end_y = 240
    
    # Corpo do pin (cilíndrico fino)
    pin_body = QRect(124, 200, 8, 40)
    pin_gradient = QLinearGradient(pin_body.left(), pin_body.top(), pin_body.right(), pin_body.top())
    pin_gradient.setColorAt(0, QColor(180, 180, 180))  # Cinza
    pin_gradient.setColorAt(0.3, QColor(240, 240, 240))  # Prata claro
    pin_gradient.setColorAt(0.5, QColor(255, 255, 255))  # Branco (brilho)
    pin_gradient.setColorAt(0.7, QColor(240, 240, 240))  # Prata claro
    pin_gradient.setColorAt(1, QColor(160, 160, 160))  # Cinza escuro
    
    painter.setBrush(pin_gradient)
    painter.setPen(QPen(QColor(130, 130, 130), 1))
    painter.drawRoundedRect(pin_body, 2, 2)
    
    # Linha de brilho no pin
    painter.setPen(QPen(QColor(255, 255, 255, 180), 1))
    painter.drawLine(126, 202, 126, 238)
    
    # Ponta do pin (cônica/afiada)
    pin_tip = QPolygon([
        QPoint(124, 240),
        QPoint(132, 240),
        QPoint(128, 250)
    ])
    painter.setBrush(QColor(120, 120, 120))
    painter.setPen(QPen(QColor(100, 100, 100), 1))
    painter.drawPolygon(pin_tip)
    
    # === BASE CIRCULAR (MAIS LARGA) ===
    base_center_x = 128
    base_center_y = 185
    base_radius = 20
    
    base_rect = QRect(base_center_x - base_radius, base_center_y - base_radius, 
                      base_radius * 2, base_radius * 2)
    
    # Gradiente radial para base (vermelho)
    base_gradient = QRadialGradient(base_center_x, base_center_y, base_radius)
    base_gradient.setColorAt(0, QColor(240, 30, 30))  # Vermelho claro (centro)
    base_gradient.setColorAt(0.6, QColor(220, 10, 10))  # Vermelho médio
    base_gradient.setColorAt(1, QColor(180, 0, 0))  # Vermelho escuro (borda)
    
    painter.setBrush(base_gradient)
    painter.setPen(QPen(QColor(160, 0, 0), 1.5))
    painter.drawEllipse(base_rect)
    
    # Indentação/anel na base (onde encontra o shaft)
    indent_radius = 12
    indent_rect = QRect(base_center_x - indent_radius, base_center_y - indent_radius,
                        indent_radius * 2, indent_radius * 2)
    indent_gradient = QRadialGradient(base_center_x, base_center_y, indent_radius)
    indent_gradient.setColorAt(0, QColor(200, 0, 0, 150))  # Vermelho escuro transparente
    indent_gradient.setColorAt(1, QColor(200, 0, 0, 0))  # Transparente
    painter.setBrush(indent_gradient)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(indent_rect)
    
    # === SHAFT/CORPO CILÍNDRICO (COM INDENTAÇÃO) ===
    shaft_top = 140
    shaft_bottom = 180
    shaft_width = 16
    shaft_center_x = 128
    
    # Corpo do shaft
    shaft_rect = QRect(shaft_center_x - shaft_width//2, shaft_top, shaft_width, shaft_bottom - shaft_top)
    
    # Gradiente para shaft (vermelho)
    shaft_gradient = QLinearGradient(shaft_rect.left(), shaft_rect.top(), shaft_rect.right(), shaft_rect.top())
    shaft_gradient.setColorAt(0, QColor(200, 0, 0))  # Vermelho escuro (sombra esquerda)
    shaft_gradient.setColorAt(0.3, QColor(240, 20, 20))  # Vermelho médio
    shaft_gradient.setColorAt(0.5, QColor(255, 40, 40))  # Vermelho claro (centro)
    shaft_gradient.setColorAt(0.7, QColor(240, 20, 20))  # Vermelho médio
    shaft_gradient.setColorAt(1, QColor(180, 0, 0))  # Vermelho escuro (sombra direita)
    
    painter.setBrush(shaft_gradient)
    painter.setPen(QPen(QColor(160, 0, 0), 1))
    painter.drawRoundedRect(shaft_rect, 8, 8)
    
    # Indentação/anel superior (onde encontra a cabeça)
    indent_top_radius = 10
    indent_top_rect = QRect(shaft_center_x - indent_top_radius, shaft_top - 2,
                           indent_top_radius * 2, indent_top_radius * 2)
    indent_top_gradient = QRadialGradient(shaft_center_x, shaft_top, indent_top_radius)
    indent_top_gradient.setColorAt(0, QColor(180, 0, 0, 180))  # Vermelho escuro
    indent_top_gradient.setColorAt(1, QColor(180, 0, 0, 0))  # Transparente
    painter.setBrush(indent_top_gradient)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(indent_top_rect)
    
    # Indentação/anel inferior (onde encontra a base)
    indent_bottom_radius = 10
    indent_bottom_rect = QRect(shaft_center_x - indent_bottom_radius, shaft_bottom - 2,
                              indent_bottom_radius * 2, indent_bottom_radius * 2)
    indent_bottom_gradient = QRadialGradient(shaft_center_x, shaft_bottom, indent_bottom_radius)
    indent_bottom_gradient.setColorAt(0, QColor(180, 0, 0, 180))  # Vermelho escuro
    indent_bottom_gradient.setColorAt(1, QColor(180, 0, 0, 0))  # Transparente
    painter.setBrush(indent_bottom_gradient)
    painter.drawEllipse(indent_bottom_rect)
    
    # === CABEÇA DOMED (TOPO ARREDONDADO) ===
    head_center_x = 128
    head_center_y = 110
    head_radius = 32
    
    head_rect = QRect(head_center_x - head_radius, head_center_y - head_radius,
                      head_radius * 2, head_radius * 2)
    
    # Gradiente radial para cabeça domed (vermelho glossy)
    head_gradient = QRadialGradient(head_center_x, head_center_y, head_radius)
    head_gradient.setColorAt(0, QColor(255, 80, 80))  # Vermelho muito claro (centro/brilho)
    head_gradient.setColorAt(0.2, QColor(255, 50, 50))  # Vermelho claro
    head_gradient.setColorAt(0.4, QColor(240, 30, 30))  # Vermelho médio
    head_gradient.setColorAt(0.7, QColor(220, 15, 15))  # Vermelho
    head_gradient.setColorAt(1, QColor(200, 0, 0))  # Vermelho escuro (borda)
    
    painter.setBrush(head_gradient)
    painter.setPen(QPen(QColor(180, 0, 0), 1.5))
    painter.drawEllipse(head_rect)
    
    # === HIGHLIGHTS BRANCOS GLOSSY ===
    # Highlight principal no topo (especular)
    highlight1_x = head_center_x - 18
    highlight1_y = head_center_y - 18
    highlight1_size = 16
    highlight1_rect = QRect(highlight1_x, highlight1_y, highlight1_size, highlight1_size)
    highlight1_gradient = QRadialGradient(highlight1_rect.center().x(), highlight1_rect.center().y(), highlight1_size//2)
    highlight1_gradient.setColorAt(0, QColor(255, 255, 255, 255))  # Branco total
    highlight1_gradient.setColorAt(0.4, QColor(255, 200, 200, 150))  # Vermelho claro transparente
    highlight1_gradient.setColorAt(1, QColor(255, 200, 200, 0))  # Transparente
    painter.setBrush(highlight1_gradient)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(highlight1_rect)
    
    # Highlight secundário menor (mais intenso)
    highlight2_x = head_center_x - 10
    highlight2_y = head_center_y - 10
    highlight2_size = 8
    highlight2_rect = QRect(highlight2_x, highlight2_y, highlight2_size, highlight2_size)
    highlight2_gradient = QRadialGradient(highlight2_rect.center().x(), highlight2_rect.center().y(), highlight2_size//2)
    highlight2_gradient.setColorAt(0, QColor(255, 255, 255, 255))  # Branco total
    highlight2_gradient.setColorAt(1, QColor(255, 255, 255, 0))  # Transparente
    painter.setBrush(highlight2_gradient)
    painter.drawEllipse(highlight2_rect)
    
    # Highlight na borda direita (curvatura)
    highlight3_x = head_center_x + 12
    highlight3_y = head_center_y - 5
    highlight3_width = 18
    highlight3_height = 25
    highlight3_rect = QRect(highlight3_x, highlight3_y, highlight3_width, highlight3_height)
    highlight3_gradient = QLinearGradient(highlight3_rect.left(), highlight3_rect.top(), highlight3_rect.right(), highlight3_rect.top())
    highlight3_gradient.setColorAt(0, QColor(255, 150, 150, 140))  # Vermelho claro transparente
    highlight3_gradient.setColorAt(1, QColor(255, 150, 150, 0))  # Transparente
    painter.setBrush(highlight3_gradient)
    painter.drawEllipse(highlight3_rect)
    
    # Highlight na borda esquerda (curvatura)
    highlight4_x = head_center_x - 30
    highlight4_y = head_center_y - 3
    highlight4_width = 15
    highlight4_height = 20
    highlight4_rect = QRect(highlight4_x, highlight4_y, highlight4_width, highlight4_height)
    highlight4_gradient = QLinearGradient(highlight4_rect.right(), highlight4_rect.top(), highlight4_rect.left(), highlight4_rect.top())
    highlight4_gradient.setColorAt(0, QColor(255, 120, 120, 100))  # Vermelho claro transparente
    highlight4_gradient.setColorAt(1, QColor(255, 120, 120, 0))  # Transparente
    painter.setBrush(highlight4_gradient)
    painter.drawEllipse(highlight4_rect)
    
    # Borda sutil na cabeça
    painter.setBrush(Qt.NoBrush)
    painter.setPen(QPen(QColor(150, 0, 0), 1))
    painter.drawEllipse(head_rect)
    
    painter.end()
    
    # Salvar
    pixmap.save('alfinete_vermelho.png', 'PNG')
    print("[OK] alfinete_vermelho.png criado (exato como imagem)!")
    
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
    create_exact_pin()

