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
    
    # Ler o arquivo version.py
    version_file = os.path.join(moviepy_path, 'version.py')
    if os.path.exists(version_file):
        print(f"\nConteúdo do arquivo version.py:")
        with open(version_file, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                print(f"Linha {i+1}: {line.rstrip()}")
    else:
        print("Arquivo version.py não encontrado!")
else:
    print("MoviePy não encontrado em nenhum diretório site-packages!")