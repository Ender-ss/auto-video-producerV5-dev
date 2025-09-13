import sys
import os

print("Procurando instalações do MoviePy...")
site_packages = [p for p in sys.path if 'site-packages' in p]

for path in site_packages:
    print(f"\nVerificando: {path}")
    if os.path.exists(path):
        moviepy_dirs = [d for d in os.listdir(path) if 'moviepy' in d.lower()]
        if moviepy_dirs:
            print(f"  Encontrados diretórios MoviePy: {moviepy_dirs}")
            for dir_name in moviepy_dirs:
                dir_path = os.path.join(path, dir_name)
                if os.path.isdir(dir_path):
                    print(f"  Diretório: {dir_path}")
                    # Verificar se há um arquivo __init__.py
                    init_file = os.path.join(dir_path, '__init__.py')
                    if os.path.exists(init_file):
                        print(f"    Arquivo __init__.py encontrado")
                        # Ler as primeiras linhas para ver a versão
                        with open(init_file, 'r') as f:
                            lines = f.readlines()[:10]  # Ler as primeiras 10 linhas
                            for i, line in enumerate(lines):
                                if '__version__' in line:
                                    print(f"    Linha {i+1}: {line.strip()}")
                    
                    # Verificar se há um subdiretório editor
                    editor_dir = os.path.join(dir_path, 'editor')
                    if os.path.exists(editor_dir):
                        print(f"    Subdiretório editor encontrado")
                        editor_init = os.path.join(editor_dir, '__init__.py')
                        if os.path.exists(editor_init):
                            print(f"      Arquivo editor/__init__.py encontrado")
                        else:
                            print(f"      Arquivo editor/__init__.py NÃO encontrado")
                    else:
                        print(f"    Subdiretório editor NÃO encontrado")
        else:
            print("  Nenhum diretório MoviePy encontrado")
    else:
        print(f"  Diretório não existe: {path}")

print("\nVerificação concluída!")