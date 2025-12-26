"""
Converte Alfinete 3d.png para .ico
"""

from PIL import Image
import os

def convert_to_ico():
    """Converte Alfinete 3d.png para .ico"""
    input_file = "Alfinete 3d.png"
    output_file = "alfinete_vermelho.ico"
    
    if not os.path.exists(input_file):
        print(f"[ERRO] Arquivo {input_file} não encontrado!")
        return
    
    try:
        # Abrir imagem
        img = Image.open(input_file)
        
        # Converter para RGBA se necessário
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Redimensionar para tamanhos padrão e salvar como ICO
        # PIL precisa que a imagem seja quadrada para ICO
        sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
        
        # Criar lista de imagens redimensionadas
        images = []
        for size in sizes:
            resized = img.resize(size, Image.Resampling.LANCZOS)
            images.append(resized)
        
        # Salvar como ICO
        img.save(output_file, format='ICO', sizes=[(s[0], s[1]) for s in sizes])
        
        print(f"[OK] {output_file} criado com sucesso!")
        
    except Exception as e:
        print(f"[ERRO] Erro ao converter: {e}")
        # Tentar método alternativo
        try:
            # Salvar apenas o tamanho original como ICO
            img_256 = img.resize((256, 256), Image.Resampling.LANCZOS)
            img_256.save(output_file, format='ICO')
            print(f"[OK] {output_file} criado (tamanho único)!")
        except Exception as e2:
            print(f"[ERRO] Método alternativo também falhou: {e2}")

if __name__ == '__main__':
    convert_to_ico()
