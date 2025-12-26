"""
Extrai PNGs do alfinete_verde.ico para usar no projeto
Baseado no ícone oficial da identidade visual
"""

from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QImage
from PySide6.QtCore import Qt
import sys

def remove_white_background(pixmap):
    """Remove fundo branco do pixmap, tornando-o transparente"""
    # Converter pixmap para imagem para acessar pixels
    image = pixmap.toImage()
    
    # Converter para formato ARGB32 para suportar transparência
    image = image.convertToFormat(QImage.Format_ARGB32)
    
    # Criar máscara de transparência - remover pixels brancos
    transparent_color = QColor(0, 0, 0, 0).rgba()  # RGBA transparente
    
    for x in range(image.width()):
        for y in range(image.height()):
            color = QColor(image.pixel(x, y))
            r, g, b, a = color.red(), color.green(), color.blue(), color.alpha()
            
            # Se for branco ou muito próximo de branco (R, G, B > 235), tornar transparente
            # Também considerar se o alpha já é baixo (já transparente)
            if a < 10:  # Já transparente
                image.setPixel(x, y, transparent_color)
            elif r > 235 and g > 235 and b > 235:  # Branco ou quase branco
                image.setPixel(x, y, transparent_color)
    
    # Converter de volta para QPixmap
    transparent_pixmap = QPixmap.fromImage(image)
    return transparent_pixmap

def extract_icon_pngs():
    """Extrai PNGs em múltiplos tamanhos do alfinete_verde.ico com fundo transparente"""
    icon_file = "alfinete_verde.ico"
    
    try:
        # Carregar ícone
        icon = QIcon(icon_file)
        
        if icon.isNull():
            print(f"ERRO: Nao foi possivel carregar {icon_file}")
            return False
        
        # Tamanhos para extrair
        sizes = [16, 24, 32, 48, 64, 128, 256]
        
        print(f"Extraindo PNGs de {icon_file} com fundo transparente...")
        
        for size in sizes:
            # Criar pixmap com fundo transparente
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)  # Fundo transparente
            
            # Obter ícone e desenhar no pixmap transparente
            icon_pixmap = icon.pixmap(size, size, QIcon.Normal, QIcon.On)
            
            if not icon_pixmap.isNull():
                # Remover fundo branco do ícone
                icon_clean = remove_white_background(icon_pixmap)
                
                # Criar painter para desenhar no pixmap transparente
                painter = QPainter(pixmap)
                painter.setRenderHint(QPainter.Antialiasing)
                painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
                # Desenhar apenas o ícone (sem fundo branco)
                painter.drawPixmap(0, 0, icon_clean)
                painter.end()
                
                # Salvar como PNG (com transparência)
                filename = f"icon_{size}.png"
                pixmap.save(filename, "PNG")
                print(f"  - {filename} ({size}x{size}) criado com fundo transparente")
            else:
                print(f"  - AVISO: Nao foi possivel criar {size}x{size}")
        
        # Salvar também como icon.png (256x256) com fundo transparente
        pixmap_256 = QPixmap(256, 256)
        pixmap_256.fill(Qt.transparent)
        icon_pixmap_256 = icon.pixmap(256, 256, QIcon.Normal, QIcon.On)
        if not icon_pixmap_256.isNull():
            # Remover fundo branco do ícone
            icon_clean_256 = remove_white_background(icon_pixmap_256)
            
            painter = QPainter(pixmap_256)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painter.drawPixmap(0, 0, icon_clean_256)
            painter.end()
            pixmap_256.save("icon.png", "PNG")
            print(f"  - icon.png (256x256) criado com fundo transparente")
        
        print("\nIcones extraidos com sucesso!")
        print("Todos os arquivos PNG foram criados com fundo TRANSPARENTE")
        return True
        
    except Exception as e:
        print(f"ERRO ao extrair icones: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    extract_icon_pngs()
    app.quit()

