import sys
import os

# Encontrar o diretório de instalação do MoviePy
site_packages = [p for p in sys.path if 'site-packages' in p]
moviepy_path = None

for path in site_packages:
    moviepy_dir = os.path.join(path, 'moviepy')
    if os.path.exists(moviepy_dir) and os.path.isdir(moviepy_dir):
        moviepy_path = moviepy_dir
        break

if moviepy_path:
    print(f"MoviePy encontrado em: {moviepy_path}")
    
    # Ler o arquivo __init__.py
    init_file = os.path.join(moviepy_path, '__init__.py')
    if os.path.exists(init_file):
        print(f"\nConteúdo do arquivo __init__.py:")
        with open(init_file, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                print(f"Linha {i+1}: {line.rstrip()}")
    else:
        print("Arquivo __init__.py não encontrado!")
    
    # Listar todos os arquivos e diretórios no diretório moviepy
    print(f"\nConteúdo do diretório moviepy:")
    for item in os.listdir(moviepy_path):
        item_path = os.path.join(moviepy_path, item)
        if os.path.isdir(item_path):
            print(f"  DIR:  {item}/")
        else:
            print(f"  FILE: {item}")
else:
    print("MoviePy não encontrado em nenhum diretório site-packages!")