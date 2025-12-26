"""
Converte Alfinete 3d.png para .ico corretamente
"""

from PIL import Image
import os

def convert_to_ico():
    input_file = "Alfinete 3d.png"
    output_file = "alfinete_vermelho_temp.ico"
    
    if not os.path.exists(input_file):
        print(f"[ERRO] {input_file} não encontrado!")
        return False
    
    try:
        img = Image.open(input_file)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Redimensionar para 256x256
        img_256 = img.resize((256, 256), Image.Resampling.LANCZOS)
        
        # Salvar como ICO
        img_256.save(output_file, format='ICO')
        
        # Renomear para o arquivo final
        if os.path.exists("alfinete_vermelho.ico"):
            os.remove("alfinete_vermelho.ico")
        os.rename(output_file, "alfinete_vermelho.ico")
        
        print("[OK] ICO criado com sucesso!")
        return True
    except Exception as e:
        print(f"[ERRO] {e}")
        return False

if __name__ == '__main__':
    convert_to_ico()

