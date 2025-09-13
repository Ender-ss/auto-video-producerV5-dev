import sys
import os
import shutil

print("Procurando diretórios site-packages...")
site_packages = [p for p in sys.path if 'site-packages' in p]

for path in site_packages:
    print(f"\nVerificando: {path}")
    if os.path.exists(path):
        moviepy_dirs = [d for d in os.listdir(path) if 'moviepy' in d.lower()]
        if moviepy_dirs:
            print(f"  Encontrados diretórios MoviePy: {moviepy_dirs}")
            for dir_name in moviepy_dirs:
                dir_path = os.path.join(path, dir_name)
                print(f"  Removendo: {dir_path}")
                try:
                    if os.path.isdir(dir_path):
                        shutil.rmtree(dir_path)
                        print(f"  ✓ Diretório {dir_path} removido com sucesso")
                    else:
                        os.remove(dir_path)
                        print(f"  ✓ Arquivo {dir_path} removido com sucesso")
                except Exception as e:
                    print(f"  ✗ Erro ao remover {dir_path}: {e}")
        else:
            print("  Nenhum diretório MoviePy encontrado")
    else:
        print(f"  Diretório não existe: {path}")

print("\nVerificação concluída!")