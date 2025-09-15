import os
import sys
from PIL import Image

# Diretório das imagens
images_dir = r'c:\Users\Enderson\Documents\APP 2\auto-video-producerV5-dev\backend\projects\a98c0799-b28c-4ead-8c85-4a4758855b0c\images'

print("Verificando imagens no diretório:", images_dir)
print("-" * 50)

# Listar todos os arquivos de imagem
image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
print(f"Encontrados {len(image_files)} arquivos de imagem:")

for i, image_file in enumerate(image_files, 1):
    image_path = os.path.join(images_dir, image_file)
    try:
        # Abrir a imagem com PIL
        with Image.open(image_path) as img:
            print(f"\nImagem {i}: {image_file}")
            print(f"  - Formato: {img.format}")
            print(f"  - Tamanho: {img.size} pixels")
            print(f"  - Modo: {img.mode}")
            print(f"  - Tamanho do arquivo: {os.path.getsize(image_path)} bytes")
            
            # Verificar se a imagem é válida
            img.verify()
            print(f"  - Status: OK (imagem válida)")
            
    except Exception as e:
        print(f"\nImagem {i}: {image_file}")
        print(f"  - Erro: {str(e)}")

print("\n" + "-" * 50)
print("Verificação concluída.")